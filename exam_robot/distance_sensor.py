import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
import random

class DistanceSensorNode(Node):
    def __init__(self):
        super().__init__('distance_sensor')
        self.publisher_ = self.create_publisher(Float32, '/distance', 10)
        self.subscription = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        
        self.distance = 5.0
        self.speed = 0.0
        self.get_logger().info('Distance sensor node started')

    def cmd_vel_callback(self, msg):
        self.speed = msg.linear.x
        self.get_logger().info(f'Received speed: {self.speed:.2f}')

    def timer_callback(self):
        # Изменяем расстояние в зависимости от скорости
        if abs(self.speed) > 0.01:
            self.distance -= abs(self.speed) * 0.3
            self.distance += random.uniform(-0.1, 0.1)
        else:
            self.distance += (5.0 - self.distance) * 0.1
            
        self.distance = max(0.1, min(10.0, self.distance))
        
        msg = Float32()
        msg.data = self.distance
        self.publisher_.publish(msg)
        self.get_logger().info(f'Distance: {msg.data:.2f}m')

def main(args=None):
    rclpy.init(args=args)
    node = DistanceSensorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()