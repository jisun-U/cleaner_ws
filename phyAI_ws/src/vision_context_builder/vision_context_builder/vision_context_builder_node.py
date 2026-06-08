#!/usr/bin/env python3
import json
import numpy as np
import cv2
from cv_bridge import CvBridge

import rclpy
from rclpy.node import Node

from yolov8_msgs.msg import DetectionArray
from std_msgs.msg import String
from sensor_msgs.msg import Image, CompressedImage


class VisionContextBuilder(Node):
    def __init__(self):
        super().__init__('vision_context_builder')

        # 파라미터 설정. 기본 해상도 파라미터, depth
        self.declare_parameter("frame_w_default", 1280)
        self.declare_parameter("frame_h_default", 720)
        self.declare_parameter("depth_topic", "/depth")
        self.frame_w = int(self.get_parameter("frame_w_default").value)
        self.frame_h = int(self.get_parameter("frame_h_default").value)
        self.depth_topic = str(self.get_parameter("depth_topic").value)

        # CV Bridge(ROS 이미지 메세지와 opencv 이미지 간 변환) 및 이미지 퍼블리셔 초기화
        self.cv_bridge = CvBridge()
        self.latest_cv_image = None # 최신 프레임 저장용
        self._log_counter = 0 # 이미지 수신 카운터, 디버그용

        # snapshot 
        self.create_subscription(String, '/vision/snapshot_req', self.on_snapshot_req, 10) # 스냅샷 요청 수신용
        self.pub_snapshot_img = self.create_publisher(CompressedImage, '/system2/snapshot/image', 10) # 퍼블리셔 객체를 만든 것일 뿐, 실제 메시지는 on_snapshot_req에서 publish 호출
        self.pub_snapshot_info = self.create_publisher(String, '/system2/snapshot/info', 10)


        # Subscribe : /tracking, RGB image, depth image
        self.subscription = self.create_subscription(
            DetectionArray,
            '/yolo/tracking',
            self.detections_callback,
            10
        )
        self.img_sub = self.create_subscription(
            Image,
            '/yolo/image_raw',
            self.image_cb,
            10
        )
        self.depth_img = None          # numpy array (H,W), single channel, meters
        self.depth_encoding = None # depth 이미지 인코딩 형식 저장 (32FC1 또는 16UC1)
        self.depth_sub = self.create_subscription(
            Image,
            self.depth_topic,          # 토픽 이름
            self.depth_cb,
            10
        )

        # Publish : 사람이 읽는 텍스트, JSON(raw)
        self.publisher_ = self.create_publisher(String, '/vision_context', 10)   # 사람이 읽는 텍스트
        self.raw_pub = self.create_publisher(String, '/vision_context_raw', 10)  # 정규화된 RAW(JSON)
        self.get_logger().info(f'VisionContextBuilder node started. (depth_topic={self.depth_topic})')


    # 프레임 크기 동적 갱신 및 openCV
    def image_cb(self, msg: Image):
        """이미지가 들어올 때마다 호출됨"""
        self.frame_w = int(msg.width)
        self.frame_h = int(msg.height)

        # 디버그 1: 이미지가 진짜 들어오고 있는지 확인 (60프레임마다 1번만 출력)
        self._log_counter += 1
        if self._log_counter % 60 == 1:
            try:
                raw_data = np.frombuffer(msg.data, dtype=np.uint8) # numpy array로 변환
                is_all_black = (np.max(raw_data) == 0) if len(raw_data) > 0 else True
                avg_val = np.mean(raw_data) if len(raw_data) > 0 else 0
                
                status = "ALL BLACK (0)" if is_all_black else f"OK (Avg: {avg_val:.1f})"
                
                self.get_logger().info(
                    f"[Vision] Image Recv: {msg.width}x{msg.height}, Enc: {msg.encoding}, Status: {status}"
                )
            except Exception as e:
                self.get_logger().warn(f"[Vision] Debug check failed: {e}")

        try:
            # ROS Image -> CV2 변환
            # openCV는 보통 BGR8을 선호하지만, 들어오는 인코딩이 다를 수 있으므로 유연하게 처리
            if msg.encoding == "bgr8":
                self.latest_cv_image = self.cv_bridge.imgmsg_to_cv2(msg, "bgr8")
            else:
                # 다른 인코딩이면 변환 시도 (rgb8 등)
                self.latest_cv_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8") 
                
        except Exception as e:
            self.get_logger().error(f"[Vision] CV Bridge Failed: {e}")

    def on_snapshot_req(self, msg: String):
        """스냅샷 요청이 왔을 때"""
        self.get_logger().info("[Vision] Snapshot Request Received!")

        if self.latest_cv_image is None:
            self.get_logger().error("[Vision] Request received but 'latest_cv_image' is None! (No image from topic yet)")
            return

        # 디버그 2: 보내기 직전 이미지 상태 확인(black인지, 크기 등)
        if np.max(self.latest_cv_image) == 0:
             self.get_logger().warn("[Vision] Sending Snapshot, but the image is PURE BLACK!")

        try:
            # JPG 압축
            success, jpg_data = cv2.imencode('.jpg', self.latest_cv_image)
            if success:
                cmp_msg = CompressedImage() #객체 생성
                cmp_msg.header.stamp = self.get_clock().now().to_msg() # 타임스탬프, 헤더에 기록
                cmp_msg.format = "jpeg"
                cmp_msg.data = jpg_data.tobytes() #
                
                self.pub_snapshot_img.publish(cmp_msg) # system2/snapshot/image publish
                self.pub_snapshot_info.publish(msg) # system2/snapshot/info publish / 스냅샷 요청
                
                self.get_logger().info(f"[Vision] Snapshot SENT to System2 (Size: {len(cmp_msg.data)} bytes)")
            else:
                self.get_logger().error("[Vision] cv2.imencode failed")
            
        except Exception as e:
            self.get_logger().error(f"[Vision] Snapshot processing failed: {e}")

    
    # depth 콜백: 32FC1(m) 또는 16UC1(mm) 처리(numpy 배열로 변환하여 self.depth_img에 저장)
    def depth_cb(self, msg: Image):
        try:
            self.depth_encoding = msg.encoding
            if msg.encoding == "32FC1":
                arr = np.frombuffer(msg.data, dtype=np.float32).reshape(msg.height, msg.width)
                self.depth_img = arr  # already meters
            elif msg.encoding in ("16UC1", "mono16"):
                arr = np.frombuffer(msg.data, dtype=np.uint16).reshape(msg.height, msg.width).astype(np.float32)
                self.depth_img = arr / 1000.0  # mm -> m
            else:
                self.depth_img = None
                self.get_logger().warn(f"[vision] unsupported depth encoding: {msg.encoding}")
        except Exception as e:
            self.depth_img = None
            self.get_logger().warn(f"[vision] depth parse failed: {e}")

    # 화면 내 상대 위치 설명(현재 프레임 크기 기준)
    def describe_position(self, x, y):
        width, height = self.frame_w, self.frame_h
        horizontal = "왼쪽" if x < width // 2 else "오른쪽"
        vertical = "위" if y < height // 2 else "아래"
        return f"{vertical} {horizontal}"

    # bbox 중심 주변 median depth(m) 계산 (depth 없으면 None)
    def _estimate_range_from_depth(self, cx, cy, w, h):
        if self.depth_img is None:
            return None
        try:
            H, W = self.depth_img.shape
        except Exception:
            return None

        # 중심 주변 작은 윈도우 (bbox의 20% 크기, 최소 5px)
        win = int(max(5, min(w, h) * 0.2)) if (w is not None and h is not None) else 10
        x0 = max(0, int(cx - win // 2)); x1 = min(W, int(cx + win // 2))
        y0 = max(0, int(cy - win // 2)); y1 = min(H, int(cy + win // 2))
        if x1 <= x0 or y1 <= y0:
            return None

        roi = self.depth_img[y0:y1, x0:x1]
        if roi.size == 0:
            return None

        # 유효 거리만 필터 (0.1m ~ 50m)
        valid = roi[np.isfinite(roi)]
        valid = valid[(valid > 0.1) & (valid < 50.0)]
        if valid.size < 10:
            return None

        return float(np.median(valid))

    def detections_callback(self, msg: DetectionArray):
        context_sentences = [] # 사람이 읽는 텍스트 메시지용 리스트
        raw_objects = [] # JSON(raw) 메시지용 리스트

        for det in msg.detections:
            try:
                # id는 문자열로 통일(Executor/Tracker 비교 안정성을 위해)
                obj_id = str(det.id)
                cls = det.class_name

                # center 추출
                x = int(det.bbox.center.position.x)
                y = int(det.bbox.center.position.y)

                # bbox w/h 있으면 함께 기록(없어도 OK)
                w = None
                h = None
                try:
                    w = float(getattr(det.bbox.size, 'x'))
                    h = float(getattr(det.bbox.size, 'y'))
                except Exception:
                    w = None
                    h = None

                position_desc = self.describe_position(x, y) # 중심 좌표 x,y를 통한 화면 위치 (ex. 오른쪽 위, 왼쪽 아래 등)
                sentence = f"{obj_id}번 객체는 {cls}이며 화면 {position_desc}에 위치해 있습니다."
                context_sentences.append(sentence) # 모든 객체의 설명을 리스트에 추가

                raw_obj = {
                    "id": obj_id,            # 문자열로 통일
                    "class": cls,
                    "center": {"x": x, "y": y}
                }
                if w is not None and h is not None:
                    raw_obj["bbox"] = {"w": w, "h": h}

                    # depth → range_m 추정
                    rng = self._estimate_range_from_depth(x, y, w, h) # 객체가 카메라에서 몇 m 떨어져 있는지 추정 (depth 이미지 기반, 단위: m)
                    if rng is not None:
                        raw_obj["range_m"] = float(rng)

                raw_objects.append(raw_obj)

            except Exception as e:
                self.get_logger().warn(f"[vision] Skipping detection due to error: {str(e)}")

        if not context_sentences:
            # 감지 없음 → 전송 생략
            return

        # 사람이 읽는 텍스트 메시지
        combined_text = " / ".join(context_sentences)
        self.publisher_.publish(String(data=combined_text))

        # JSON(raw) 메시지: frame 크기를 함께 보냄 
        raw_payload = {
            "frame_w": self.frame_w,
            "frame_h": self.frame_h,
            "objects": raw_objects
        }
        self.raw_pub.publish(String(data=json.dumps(raw_payload, ensure_ascii=False)))


def main(args=None):
    rclpy.init(args=args)
    node = VisionContextBuilder()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
