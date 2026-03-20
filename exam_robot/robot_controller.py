import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class RobotControllerNode(Node):
    def __init__(self):
        super().__init__('robot_controller')
        
        # Объявляем параметр
        self.declare_parameter('max_speed', 0.3)
        self.max_speed = self.get_parameter('max_speed').value
        
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.sub_status = self.create_subscription(
            String, '/robot_status', self.status_callback, 10)
        
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        self.current_status = "ALL OK"
        self.last_status = ""
        self.get_logger().info(f'Robot controller started (max speed: {self.max_speed} m/s)')

    def status_callback(self, msg):
        self.current_status = msg.data
        if self.current_status != self.last_status:
            self.get_logger().info(f'Status received: {self.current_status}')
            self.last_status = self.current_status

    def get_twist_command(self):
        twist = Twist()
        
        if self.current_status == "ALL OK":
            twist.linear.x = self.max_speed
            twist.angular.z = 0.0
            
        elif self.current_status == "WARNING: Low battery":
            twist.linear.x = self.max_speed / 3
            twist.angular.z = 0.0
            
        elif self.current_status == "WARNING: Obstacle close":
            twist.linear.x = 0.0
            twist.angular.z = 0.5
            
        elif self.current_status == "CRITICAL":
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            
        else:
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            
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
