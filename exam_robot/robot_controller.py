import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String
from geometry_msgs.msg import Twist

class RobotControllerNode(Node):
    def __init__(self):
        super().__init__('robot_controller')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.sub_battery = self.create_subscription(
            Float32, '/battery_level', self.battery_callback, 10)
        self.sub_distance = self.create_subscription(
            Float32, '/distance', self.distance_callback, 10)
        self.sub_status = self.create_subscription(
            String, '/robot_status', self.status_callback, 10)
        
        self.timer = self.create_timer(0.5, self.timer_callback)
        
        self.battery_level = 100.0
        self.distance = 5.0
        self.status = ""
        self.get_logger().info('Robot controller node started')

    def battery_callback(self, msg):
        self.battery_level = msg.data

    def distance_callback(self, msg):
        self.distance = msg.data

    def status_callback(self, msg):
        self.status = msg.data

    def timer_callback(self):
        twist_msg = Twist()
        
        # Логика управления
        if self.battery_level < 20:
            # Батарея разряжена - останов
            twist_msg.linear.x = 0.0
            twist_msg.angular.z = 0.0
            self.get_logger().warn('Battery low - stopping!')
        elif self.distance < 0.5:
            # Слишком близко к препятствию - назад и поворот
            twist_msg.linear.x = -0.1
            twist_msg.angular.z = 0.5
            self.get_logger().warn('Obstacle too close - backing up!')
        elif self.distance < 1.5:
            # Приближаемся к препятствию - замедляемся и поворачиваем
            twist_msg.linear.x = 0.1
            twist_msg.angular.z = 0.3
            self.get_logger().info('Obstacle ahead - slowing down')
        else:
            # Свободный путь - едем прямо
            twist_msg.linear.x = 0.2
            twist_msg.angular.z = 0.0
            self.get_logger().info('Clear path - moving forward')
        
        self.publisher_.publish(twist_msg)

def main(args=None):
    rclpy.init(args=args)
    node = RobotControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()