# Copyright (C) 2023  Miguel Ángel González Santamarta

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from typing import List, Dict

import rclpy
from rclpy.qos import qos_profile_sensor_data
from rclpy.node import Node
import torch

from cv_bridge import CvBridge

from ultralytics import YOLO
from ultralytics.engine.results import Results
from ultralytics.engine.results import Boxes
from ultralytics.engine.results import Masks
from ultralytics.engine.results import Keypoints

from sensor_msgs.msg import Image
from yolov8_msgs.msg import Point2D
from yolov8_msgs.msg import BoundingBox2D
from yolov8_msgs.msg import Mask
from yolov8_msgs.msg import KeyPoint2D
from yolov8_msgs.msg import KeyPoint2DArray
from yolov8_msgs.msg import Detection
from yolov8_msgs.msg import DetectionArray
from std_srvs.srv import SetBool


_original_torch_load = torch.load


def _trusted_torch_load(*args, **kwargs):
    # Trusted local YOLO checkpoints created before PyTorch 2.6 may require
    # full pickle loading because weights_only=True is now the default.
    kwargs.setdefault("weights_only", False)
    return _original_torch_load(*args, **kwargs)


torch.load = _trusted_torch_load


class Yolov8Node(Node):

    def __init__(self) -> None: # 보통 객체가 시작될 때 필요한 초기값을 설정
        super().__init__("yolov8_node")

        # params
        self.declare_parameter("model", "yolov8m.pt")
        model = self.get_parameter(
            "model").get_parameter_value().string_value

        self.declare_parameter("device", "cuda:0") 
        #첫 번째GPU 사용할때 / CPU 사용하고 싶으면 "cpu"로 바꾸기
        self.device = self.get_parameter(
            "device").get_parameter_value().string_value

        self.declare_parameter("threshold", 0.5)
        self.threshold = self.get_parameter(
            "threshold").get_parameter_value().double_value

        self.declare_parameter("enable", True)
        self.enable = self.get_parameter(
            "enable").get_parameter_value().bool_value

        self.cv_bridge = CvBridge() # 센서 메세지를 OpenCV 이미지로 변환함
        self.yolo = YOLO(model)
        self.yolo.fuse() # 가능한 레이어들을 합침

        # pubs : 추론 결과를 DetectionArray형태로 퍼블리시
        self._pub = self.create_publisher(DetectionArray, "detections", 10)

        # subs : /image_raw 토픽을 구독하여 새로운 이미지가 들어올 때마다 image_cb 콜백함수 실행
        self._sub = self.create_subscription(
            Image, "image_raw", self.image_cb,
            qos_profile_sensor_data
        )

        # services : 외부에서 enable 여부를 True/False로 제어할 수 있게하는 서비스
        self._srv = self.create_service(SetBool, "enable", self.enable_cb)

# enable_cb 서비스 콜백 : SetBool 타입의 서비스 요청을 받아 노드가 추론을 진행할지(enable=True), 중단할지(enable=False)를 진행한다.
    def enable_cb(
        self,
        req: SetBool.Request,
        res: SetBool.Response
    ) -> SetBool.Response:
        self.enable = req.data
        res.success = True
        return res

	#매개변수 results :ultralytics.engine.results.Results 타입의 객체
    def parse_hypothesis(self, results: Results) -> List[Dict]:

        hypothesis_list = [] #결과를 저장할 빈 리스트.

        box_data: Boxes
        for box_data in results.boxes:
            hypothesis = {
                "class_id": int(box_data.cls),
                "class_name": self.yolo.names[int(box_data.cls)],
                "score": float(box_data.conf)
            }
            hypothesis_list.append(hypothesis)

        return hypothesis_list

    def parse_boxes(self, results: Results) -> List[BoundingBox2D]:

        boxes_list = []

        box_data: Boxes
        for box_data in results.boxes:

            msg = BoundingBox2D()

            # get boxes values
            box = box_data.xywh[0]
            msg.center.position.x = float(box[0])
            msg.center.position.y = float(box[1])
            msg.size.x = float(box[2])
            msg.size.y = float(box[3])

            # append msg
            boxes_list.append(msg)

        return boxes_list

    def parse_masks(self, results: Results) -> List[Mask]:

        masks_list = []

        def create_point2d(x: float, y: float) -> Point2D:
            p = Point2D()
            p.x = x
            p.y = y
            return p

        mask: Masks
        for mask in results.masks:

            msg = Mask()

            msg.data = [create_point2d(float(ele[0]), float(ele[1]))
                        for ele in mask.xy[0].tolist()]
            msg.height = results.orig_img.shape[0]
            msg.width = results.orig_img.shape[1]

            masks_list.append(msg)

        return masks_list

    def parse_keypoints(self, results: Results) -> List[KeyPoint2DArray]:

        keypoints_list = []

        points: Keypoints
        for points in results.keypoints:

            msg_array = KeyPoint2DArray()

            if points.conf is None:
                continue

            for kp_id, (p, conf) in enumerate(zip(points.xy[0], points.conf[0])):

                if conf >= self.threshold: # 신뢰도가 특정 김계값 이상일때만 메세지에 추가한다.
                    msg = KeyPoint2D()

                    msg.id = kp_id + 1
                    msg.point.x = float(p[0])
                    msg.point.y = float(p[1])
                    msg.score = float(conf)

                    msg_array.data.append(msg)

            keypoints_list.append(msg_array)

        return keypoints_list

    def image_cb(self, msg: Image) -> None:

        if self.enable:

            # convert image + predict
            cv_image = self.cv_bridge.imgmsg_to_cv2(msg) #Ros image 1개를 받음 > OpenCV형식
            results = self.yolo.predict(
                source=cv_image,
                verbose=False,
                stream=False,
                conf=self.threshold,
                device=self.device
            )
            #predict함수는 한장의 이미지를 입력받아 results이미지를 여러개 반환
            #YOLO 추론 결과는 GPU메모리에 저장.여러 라이브러리(openCV,numpy)는 CPU 환경을 기준으로 설계됨
            results: Results = results[0].cpu() 

            if results.boxes:
                hypothesis = self.parse_hypothesis(results)
                boxes = self.parse_boxes(results)

            if results.masks:
                masks = self.parse_masks(results)

            if results.keypoints:
                keypoints = self.parse_keypoints(results)

            # create detection msgs
            detections_msg = DetectionArray()

            for i in range(len(results)):

                aux_msg = Detection()

                if results.boxes:
                    aux_msg.class_id = hypothesis[i]["class_id"]
                    aux_msg.class_name = hypothesis[i]["class_name"]
                    aux_msg.score = hypothesis[i]["score"]

                    aux_msg.bbox = boxes[i]

                if results.masks:
                    aux_msg.mask = masks[i]

                if results.keypoints:
                    aux_msg.keypoints = keypoints[i]

                detections_msg.detections.append(aux_msg)

            # publish detections
            detections_msg.header = msg.header
            self._pub.publish(detections_msg)


def main():
    rclpy.init() #로스 노드 초기화
    node = Yolov8Node() #YOLOv8 노드 생성
    rclpy.spin(node) #계속 이벤트 루프를 돌림
    node.destroy_node() #노드를 정리하고
    rclpy.shutdown() #로스2 종료
