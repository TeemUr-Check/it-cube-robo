import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String

class StatusDisplayNode(Node):
    def __init__(self):
        super().__init__('status_display')
        self.publisher_ = self.create_publisher(String, '/robot_status', 10)
        
        self.sub_battery = self.create_subscription(
            Float32, '/battery_level', self.battery_callback, 10)
        self.sub_distance = self.create_subscription(
            Float32, '/distance', self.distance_callback, 10)
        
        self.battery_level = 100.0
        self.distance = 5.0
        self.timer = self.create_timer(1.0, self.timer_callback)
        
        self.get_logger().info('Status display node started')

    def battery_callback(self, msg):
        self.battery_level = msg.data

    def distance_callback(self, msg):
        self.distance = msg.data

    def timer_callback(self):
        status_msg = String()
        
        # Анализ состояния
        if self.battery_level < 20:
            status_msg.data = f"LOW BATTERY! Level: {self.battery_level:.1f}%"
        elif self.distance < 1.0:
            status_msg.data = f"OBSTACLE AHEAD! Distance: {self.distance:.2f}m"
        elif self.distance < 2.0:
            status_msg.data = f"WARNING: Obstacle at {self.distance:.2f}m"
        else:
            status_msg.data = f"NORMAL: Battery {self.battery_level:.1f}%, Distance {self.distance:.2f}m"
        
        self.publisher_.publish(status_msg)
        self.get_logger().info(f'Status: {status_msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = StatusDisplayNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()