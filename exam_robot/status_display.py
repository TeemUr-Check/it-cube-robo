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
        
        self.timer = self.create_timer(0.5, self.timer_callback)  # 2 Hz
        
        self.battery_level = 100.0
        self.distance = 3.0
        self.last_status = ""
        self.get_logger().info('Status display node started')

    def battery_callback(self, msg):
        self.battery_level = msg.data

    def distance_callback(self, msg):
        self.distance = msg.data

    def get_status(self):
        # Проверка CRITICAL в первую очередь (наивысший приоритет)
        if self.battery_level < 10.0 or self.distance < 0.7:
            return "CRITICAL"
        # Затем WARNING: Low battery
        elif self.battery_level < 20.0:
            return "WARNING: Low battery"
        # Затем WARNING: Obstacle close
        elif self.distance < 1.0:
            return "WARNING: Obstacle close"
        # Иначе ALL OK
        else:
            return "ALL OK"

    def timer_callback(self):
        current_status = self.get_status()
        
        # Публикуем статус
        status_msg = String()
        status_msg.data = current_status
        self.publisher_.publish(status_msg)
        
        # Логируем только при изменении статуса
        if current_status != self.last_status:
            self.get_logger().info(f'Status changed: {current_status}')
            self.last_status = current_status
        
        # Для отладки публикуем подробности каждые 2 секунды
        self.get_logger().debug(f'Battery: {self.battery_level:.1f}%, Distance: {self.distance:.2f}m')

def main(args=None):
    rclpy.init(args=args)
    node = StatusDisplayNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
