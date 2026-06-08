
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json

class ActionInterpreterNode(Node):

    def __init__(self):
        super().__init__('action_interpreter')
        #action_sequence 토픽을 구독
        self.subscription = self.create_subscription(
            String,
            'action_sequence',
            self.action_callback,
            10
        )
        self.get_logger().info('Action Interpreter Node started.')

    #메세지가 들어올 때마다 처리
    def action_callback(self, msg: String):
        try:
            # JSON 문자열을 -> 파일선 객체로 파싱
            data = json.loads(msg.data)
            actions = data.get("actions", [])
            self.get_logger().info(f"Received actions: {actions}")

            for action_dict in actions:
                action_type = action_dict.get("action")
                parameters = action_dict.get("parameters", {})

                # 만약 parameters가 문자열이면, 다시 파싱
                if isinstance(parameters, str):
                    parameters = json.loads(parameters)

                self.interpret_action(action_type, parameters)

        except Exception as e:
            self.get_logger().error(f"Failed to interpret actions: {str(e)}")

    def interpret_action(self, action_type, parameters):
        if action_type == "rotate":
            direction = parameters.get("direction", "left")
            angle = parameters.get("angle", 90)
            self.get_logger().info(f"[ROTATE] Rotating {direction} by {angle} degrees")

        elif action_type == "scan_area":
            direction = parameters.get("direction", "left")
            duration = parameters.get("duration", 3)
            self.get_logger().info(f"[SCAN] Scanning {direction} area for {duration} seconds")

        elif action_type == "detect":
            target = parameters.get("target", "person")
            count = parameters.get("count", False)
            self.get_logger().info(f"[DETECT] Detecting {target}. Count: {count}")

        elif action_type == "highlight":
            target_id = parameters.get("target_id", 1)
            color = parameters.get("color", "red")
            self.get_logger().info(f"[HIGHLIGHT] Highlighting target ID {target_id} with {color} color")

        elif action_type == "track":
            target_id = parameters.get("target_id", 1)
            duration = parameters.get("duration", 5)
            self.get_logger().info(f"[TRACK] Tracking target ID {target_id} for {duration} seconds")

        elif action_type == "monitor":
            target_type = parameters.get("target_type", "object")
            duration = parameters.get("duration", 10)
            self.get_logger().info(f"[MONITOR] Monitoring {target_type} for {duration} seconds")

        elif action_type == "alert":
            message = parameters.get("message", "Alert triggered")
            level = parameters.get("level", "info")
            self.get_logger().info(f"[ALERT] ({level.upper()}) {message}")

        else:
            self.get_logger().warn(f"Unknown action type: {action_type}")

def main(args=None):
    rclpy.init(args=args)
    node = ActionInterpreterNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
