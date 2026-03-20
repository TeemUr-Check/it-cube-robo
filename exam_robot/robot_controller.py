import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class RobotControllerNode(Node):
    def __init__(self):
        super().__init__('robot_controller')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.sub_status = self.create_subscription(
            String, '/robot_status', self.status_callback, 10)
        
        self.timer = self.create_timer(0.1, self.timer_callback)  # 10 Hz
        
        self.current_status = "ALL OK"
        self.last_status = ""
        self.get_logger().info('Robot controller node started')

    def status_callback(self, msg):
        self.current_status = msg.data
        # Логируем изменение статуса
        if self.current_status != self.last_status:
            self.get_logger().info(f'Status received: {self.current_status}')
            self.last_status = self.current_status

    def get_twist_command(self):
        twist = Twist()
        
        # Логика движения в зависимости от статуса
        if self.current_status == "ALL OK":
            twist.linear.x = 0.3
            twist.angular.z = 0.0
            self.get_logger().debug('Command: Moving forward at 0.3 m/s')
            
        elif self.current_status == "WARNING: Low battery":
            twist.linear.x = 0.1
            twist.angular.z = 0.0
            self.get_logger().debug('Command: Moving slowly at 0.1 m/s (low battery)')
            
        elif self.current_status == "WARNING: Obstacle close":
            twist.linear.x = 0.0
            twist.angular.z = 0.5
            self.get_logger().debug('Command: Rotating at 0.5 rad/s (obstacle ahead)')
            
        elif self.current_status == "CRITICAL":
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.get_logger().debug('Command: EMERGENCY STOP')
            
        else:
            # Неизвестный статус - по умолчанию останов
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.get_logger().warn(f'Unknown status: {self.current_status}')
            
        return twist

    def timer_callback(self):
        twist_msg = self.get_twist_command()
        self.publisher_.publish(twist_msg)

def main(args=None):
    rclpy.init(args=args)
    node = RobotControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
