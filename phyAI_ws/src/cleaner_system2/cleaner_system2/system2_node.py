#!/usr/bin/env python3
import json
import threading
from typing import Optional, Any, Dict, Tuple

import cv2  # ★ GUI 갱신용 추가
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from cleaner_msgs.msg import PlanCommand
from sensor_msgs.msg import CompressedImage

from .models import System1State
from .llm_planner import build_plan_dict, summarize_final_report
from .utils.visualizer import SnapshotVisualizer


def _should_treat_as_no(user_cmd: str) -> bool:
    """운용자 입력이 '추가 명령 없음' 계열인지 판정."""
    if not user_cmd:
        return True
    s = user_cmd.strip().lower()
    if s in (
        "no", "n", "none", "skip", "pass",
        "없어", "그냥 둬", "그냥", "끝", "종료"
    ):
        return True
    return False


class System2Node(Node):
    def __init__(self):
        super().__init__('system2_node')

        # 최근 상태 캐시 (/cleaner_state 기반)
        self.latest_state: Optional[System1State] = None
        
        # 시각화 도구 초기화
        self.visualizer = SnapshotVisualizer(self.get_logger())
        
        # [핵심 1] GUI가 멈추지 않도록 주기적으로 waitKey를 호출하는 타이머 추가
        self.create_timer(0.1, self.gui_timer_callback)

        # ----------- 구독 -----------
        self.snap_img_sub = self.create_subscription(
            CompressedImage, '/system2/snapshot/image', self.on_snapshot_image, 10
        )
        self.snap_info_sub = self.create_subscription(
            String, '/system2/snapshot/info', self.on_snapshot_info, 10
        )
        self.state_sub = self.create_subscription(
            String, '/cleaner_state', self.state_callback, 10
        )
        self.user_cmd_sub = self.create_subscription(
            String, '/system2/user_command', self.user_command_callback, 10
        )
        self.final_report_sub = self.create_subscription(
            String, '/system2/final_report', self.final_report_callback, 10
        )

        # ----------- 퍼블리셔 -----------
        self.plan_cmd_pub = self.create_publisher(PlanCommand, '/system2/plan_cmd', 10)
        self.plan_log_pub = self.create_publisher(String, '/high_level_plan', 10)
        self.get_logger().info("System2Node started (Non-blocking GUI & Input).")

        # 상시 운영자 콘솔 입력 루프를 별도 스레드로 실행
        self._keyboard_thread = threading.Thread(
            target=self._operator_input_loop,
            daemon=True,
        )
        self._keyboard_thread.start()

    # [추가] GUI 갱신용 타이머 콜백
    def gui_timer_callback(self):
        # OpenCV 창 이벤트 처리를 위해 주기적으로 호출
        cv2.waitKey(1)

    # ----------- /snapshot 콜백 -----------
    def on_snapshot_image(self, msg: CompressedImage):
        self.get_logger().info(f"[System2] Snapshot Image Received! ({len(msg.data)} bytes)")
        try:
            self.visualizer.update_image(msg)
        except Exception as e:
            self.get_logger().error(f"[System2] visualizer.update_image failed: {e}")

    def on_snapshot_info(self, msg: String):
        self.get_logger().info(f"[System2] Snapshot Info Received: {msg.data}")
        try:
            self.visualizer.show_popup(msg)
        except Exception as e:
            self.get_logger().error(f"[System2] visualizer.show_popup failed: {e}")

    # ----------- /cleaner_state 콜백 -----------
    def state_callback(self, msg: String):
        try:
            state_dict = json.loads(msg.data)
            self.latest_state = System1State(**state_dict)
        except Exception:
            pass

    def final_report_callback(self, msg: String):
        try:
            payload = json.loads(msg.data)
        except Exception as e:
            self.get_logger().error(f"Final report parsing failed: {e}")
            return

        mission_id = payload.get("mission_id", "")
        final_status = payload.get("final_status", "unknown")
        completed_steps = payload.get("completed_steps", 0)
        total_steps = payload.get("total_recorded_steps", 0)
        last_pose = payload.get("last_pose", {}) or {}
        vision = payload.get("vision", {}) or {}
        targets = vision.get("targets", []) or []
        history = payload.get("execution_history", []) or []

        lines = [
            "",
            "================ FINAL REPORT ================",
            f"Mission ID: {mission_id}",
            f"Final Status: {final_status}",
            f"Completed Steps: {completed_steps}/{total_steps}",
        ]

        if last_pose.get("ok", False):
            lines.append(
                "Last Pose: "
                f"({last_pose.get('x', 0.0):.2f}, {last_pose.get('y', 0.0):.2f}), "
                f"yaw={last_pose.get('yaw', 0.0):.2f}"
            )
        else:
            lines.append("Last Pose: Unknown")

        lines.append(f"Detected Targets: {len(targets)}")
        for target in targets[:5]:
            lines.append(
                "  - "
                f"class={target.get('class', 'unknown')}, "
                f"id={target.get('id', '?')}, "
                f"range={target.get('range_m', 'n/a')}"
            )

        lines.append("Execution Summary:")
        for step in history:
            result = "OK" if step.get("ok") else "FAIL"
            lines.append(
                "  - "
                f"[{step.get('idx')}] {step.get('task')} => {result} "
                f"({step.get('duration_sec', 0.0)}s)"
            )

        lines.append("=============================================")
        self.get_logger().info("\n".join(lines))

        try:
            natural_report = summarize_final_report(payload)
            self.get_logger().info(
                "\n[FINAL REPORT - NATURAL LANGUAGE]\n" + natural_report
            )
        except Exception as e:
            self.get_logger().warn(
                f"Natural-language final report generation failed: {e}"
            )

    # ----------- 공통 명령 처리 (Decision 연동 로직 추가) -----------
    def _handle_user_command_raw(self, raw: str, source: str = "user_command_topic"):
        """
        입력된 명령을 받아 독립적으로 플랜을 생성/전송합니다.
        """
        user_command, extra_context, mission_from_payload = self._parse_user_command_payload(raw)

        # 1. 명령이 없는 경우 ("그냥 둬", 엔터 등)
        if _should_treat_as_no(user_command):
            if user_command:
                self.get_logger().info("[System2] Ignored empty command.")
            return

        # 2. 명령이 있는 경우 -> LLM 플랜 생성
        self.get_logger().info(f"[System2] Generating plan for: '{user_command}'")

        try:
            try:
                plan_dict = build_plan_dict(
                    user_command=user_command,
                    system1_state=self.latest_state,
                    extra_context=extra_context,
                )
            except TypeError:
                plan_dict = build_plan_dict(user_command, self.latest_state)
        except Exception as e:
            self.get_logger().error(f"[System2] LLM plan generation failed: {e}")
            return

        # mission_id 매핑
        if mission_from_payload:
            plan_dict["mission_id"] = mission_from_payload
        self._send_plan(plan_dict, source=source)
        self.get_logger().info("[System2] Plan sent.")

        # 헬퍼: 플랜 전송 + 로그 공통 처리
    def _send_plan(self, plan_dict: Dict[str, Any], source: str = "unknown"):
        # 정규화 및 전송
        plan_dict = self._normalize_plan_for_schema(plan_dict)
        plan_str = json.dumps(plan_dict, ensure_ascii=False)

        # ------- 전체 플랜 JSON 로그 출력 -------
        try:
            pretty = json.dumps(plan_dict, ensure_ascii=False, indent=2)
            self.get_logger().info(f"[System2] ({source}) generated HighLevelPlan:\n{pretty}")
        except Exception as e:
            self.get_logger().warn(
                f"[System2] ({source}) Failed to dump plan_dict for logging: {e}"
            )

        # Plan 전송
        self.plan_cmd_pub.publish(PlanCommand(plan_json=plan_str))
        self.get_logger().info(
            f"[System2] Published /system2/plan_cmd (steps={len(plan_dict.get('steps', []))})"
        )
        self.plan_log_pub.publish(String(data=plan_str))

    # ----------- 기존 헬퍼 함수들 -----------

    def _parse_user_command_payload(self, raw: str) -> Tuple[str, Optional[Dict[str, Any]], Optional[str]]:
        raw_strip = raw.strip()
        if not raw_strip:
            return "", None, None
        try:
            obj = json.loads(raw_strip)
            if isinstance(obj, dict) and "user_command" in obj:
                return str(obj.get("user_command", "")).strip(), obj.get("context"), obj.get("mission_id")
        except Exception:
            pass
        return raw_strip, None, None

    def _normalize_plan_for_schema(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(plan, dict): return plan
        allowed_top = {"version", "mission_id", "intent", "constraints", "steps", "replan_rules"}
        for k in list(plan.keys()):
            if k not in allowed_top: plan.pop(k, None)
        if not isinstance(plan.get("version"), str): plan["version"] = "1.0.0"
        constraints = plan.get("constraints")
        if constraints is None: plan["constraints"] = []
        elif not isinstance(constraints, list): plan["constraints"] = [str(constraints)]
        replan_rules = plan.get("replan_rules")
        if replan_rules is None or not isinstance(replan_rules, dict): plan["replan_rules"] = {}
        else: plan["replan_rules"] = replan_rules
        steps = plan.get("steps")
        if not isinstance(steps, list): plan["steps"] = []; return plan
        allowed_step_keys = {"task", "params", "guard", "retry"}
        for i, step in enumerate(steps):
            if not isinstance(step, dict): continue
            for k in list(step.keys()):
                if k not in allowed_step_keys: step.pop(k, None)
            if step.get("guard") is None: step.pop("guard", None)
            try: step["retry"] = max(0, int(step.get("retry", 0)))
            except: step["retry"] = 0
            params = step.get("params")
            if not isinstance(params, dict): step["params"] = {}
            if step.get("task") == "move_to":
                goal = step["params"].get("goal")
                if not isinstance(goal, dict):
                    x = step["params"].get("x")
                    y = step["params"].get("y")
                    yaw = step["params"].get("yaw", 0.0)
                    if x is not None and y is not None:
                        step["params"]["goal"] = {"x": float(x), "y": float(y), "yaw": float(yaw)}
                        for k in ("x", "y", "z"):
                            if k in step["params"]: step["params"].pop(k)
        return plan

    def user_command_callback(self, msg: String):
        self._handle_user_command_raw(msg.data, source="user_command_topic")

    # 상시 콘솔 입력 루프 (스레드)
    def _operator_input_loop(self):
        while rclpy.ok():
            try:
                # 여기서 블로킹되어도 메인 스레드(GUI 타이머)는 돕니다.
                cmd = input("\n[System2/Command] > ")
                cmd = (cmd or "").strip()
                if not cmd:
                    continue
                # 메인 스레드의 로직 호출 (Thread-safe 가정)
                self._handle_user_command_raw(cmd, source="operator_console")
            except (EOFError, KeyboardInterrupt):
                break
            except Exception as e:
                print(f"[System2] Console Input Error: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = System2Node()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    if hasattr(node, 'visualizer'):
        node.visualizer.close()
        
    node.destroy_node()
    rclpy.shutdown()
