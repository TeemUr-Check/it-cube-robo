import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class BatteryNode(Node):
    def __init__(self):
        super().__init__('battery_node')
        self.publisher_ = self.create_publisher(Float32, '/battery_level', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.battery_level = 100.0
        self.get_logger().info('Battery node started')

    def timer_callback(self):
        msg = Float32()
        msg.data = self.battery_level
        self.publisher_.publish(msg)
        
        self.battery_level -= 1.0
        if self.battery_level < 0:
            self.battery_level = 100.0
            
        self.get_logger().info(f'Battery level: {msg.data:.1f}%')

def main(args=None):
    rclpy.init(args=args)
    node = BatteryNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
