import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import openai
import os
import json
import time


class ActionGeneratorNode(Node):
    def __init__(self):
        super().__init__("action_generator")
        # subscriber: voice command에서 자연어 명령을 받음
        self.subscription = self.create_subscription(String, "voice_command", self.callback, 10)
        # publisher: action sequence(dictionary 형태) 토픽으로 결과를 발행
        self.publisher = self.create_publisher(String, "action_sequence", 10)
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.get_logger().info("Action Generator Node started.")

    def callback(self, msg):
        # 사용자의 음성 텍스트를 로그에 출력
        user_input = msg.data
        self.get_logger().info(f"Received voice command: {user_input}")
        # 시작 시간 기록 (명령 입력 -> publish 완료까지)
        start_time = time.perf_counter()
        # GPT 호출, 모델명도 함께 받음
        action_sequence, model_name = self.get_action_sequence_from_gpt(user_input)
        # JSON 문자열로 변환
        output = String()
        output.data = json.dumps(action_sequence, ensure_ascii=False)
        # publish
        self.publisher.publish(output)
        # 경과 시간 계산
        elapsed = time.perf_counter() - start_time
        self.get_logger().info(
            f"Published action sequence: {output.data} (model={model_name}, elapsed={elapsed:.3f}s)"
        )

    def get_action_sequence_from_gpt(self, user_input):
        # 기본으로 사용할 모델 이름
        model_name = "gpt-3.5-turbo"
        try:
            system_prompt = """
You are an intelligent command interpreter for the cleaner robot project. Your task is to convert user voice commands into structured JSON action sequences.

Format: 
{
  "scenario": "sentry" | "scan" | "target" | "multi_target",
  "actions": [
    {
      "action": "<action_name>",
      "parameters": { "": , ... }
    }
  ]
}

Valid actions and parameters:
| action         | parameters |
|----------------|------------|
| monitor        | {"duration": int, "target_type": "person" or "object"} |
| track          | {"target_id": int, "continuous": true or false} |
| alert          | {"message": str, "level": "info" | "warning" | "critical"} |
| scan_area      | {"direction": "front" | "rear" | "left" | "right", "duration": int} |
| detect         | {"target": "person" | "object", "count": true or false} |
| highlight      | {"target_id": int, "color": str} |
| rotate         | {"direction": "left" | "right" | "back" | "front", "angle": int} |
| target         | {"target_id": int, "lock": true or false} |
| confirm        | {"message": str} |
| multi_target   | {"target_type": "person", "order": "ascending" | "descending", "duration": int} |
| pointer_on     | {"target_id": int, "mode": "auto" | "manual"} |

Respond only with valid JSON. Do not include explanations or markdown.

Examples:

User: "뒤를 돌아서 주변을 살펴보고 사람을 발견하면 추적해줘"  
Response: {
  "scenario": "scan",
  "actions": [
    {"action": "rotate", "parameters": {"direction": "back", "angle": 180}},
    {"action": "scan_area", "parameters": {"direction": "rear", "duration": 5}},
    {"action": "detect", "parameters": {"target": "person", "count": true}},
    {"action": "track", "parameters": {"target_id": 1, "continuous": true}}
  ]
}

User: "계속 주변을 지켜보다가 사물을 발견하면 알려줘"  
Response: {
  "scenario": "sentry",
  "actions": [
    {"action": "monitor", "parameters": {"duration": 30, "target_type": "object"}},
    {"action": "alert", "parameters": {"message": "Object detected", "level": "info"}}
  ]
}
"""
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.2,
                max_tokens=200,
            )
            reply = response['choices'][0]['message']['content']
            return json.loads(reply), model_name

        except Exception as e:
            self.get_logger().error(f"GPT API error: {e}")
            return [{
                "action": "error",
                "parameters": {"message": "Failed to generate action sequence"}
            }], model_name


def main():
    rclpy.init()
    node = ActionGeneratorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

 
