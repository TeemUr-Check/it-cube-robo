import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class BatteryNode(Node):
    def __init__(self):
        super().__init__('battery_node')
        
        # Объявляем параметр
        self.declare_parameter('discharge_rate', 1.0)
        self.discharge_rate = self.get_parameter('discharge_rate').value
        
        self.publisher_ = self.create_publisher(Float32, '/battery_level', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.battery_level = 100.0
        self.last_logged_level = 100
        self.get_logger().info(f'Battery node started (discharge rate: {self.discharge_rate}%/sec)')

    def timer_callback(self):
        if self.battery_level > 0:
            msg = Float32()
            msg.data = self.battery_level
            self.publisher_.publish(msg)
            
            current_10_percent = int(self.battery_level // 10) * 10
            if current_10_percent != self.last_logged_level and current_10_percent > 0:
                self.get_logger().info(f'Battery: {current_10_percent}%')
                self.last_logged_level = current_10_percent
            
            self.battery_level -= self.discharge_rate
            if self.battery_level < 0:
                self.battery_level = 0.0
                self.get_logger().info('Battery: 0% - discharged')
        else:
            msg = Float32()
            msg.data = 0.0
            self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = BatteryNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
