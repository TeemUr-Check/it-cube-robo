import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist

class DistanceSensorNode(Node):
    def __init__(self):
        super().__init__('distance_sensor')
        self.publisher_ = self.create_publisher(Float32, '/distance', 10)
        self.subscription = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        self.timer = self.create_timer(0.2, self.timer_callback)  # 5 Hz = 0.2 сек
        
        self.distance = 3.0  # начальное расстояние
        self.linear_x = 0.0  # текущая скорость
        self.get_logger().info('Distance sensor node started')

    def cmd_vel_callback(self, msg):
        self.linear_x = msg.linear.x
        self.get_logger().debug(f'Received speed: {self.linear_x:.2f}')

    def timer_callback(self):
        # Изменяем расстояние в зависимости от движения
        if abs(self.linear_x) < 0.01:  # стоит
            # Постепенно возвращаем к 3.0
            if self.distance < 3.0:
                self.distance += 0.2
                if self.distance > 3.0:
                    self.distance = 3.0
        elif self.linear_x > 0:  # движется вперед
            self.distance -= 0.2
            if self.distance < 0.5:
                self.distance = 0.5
                self.get_logger().info('Minimum distance reached: 0.5m')
        else:  # движется назад (linear_x < 0)
            self.distance += 0.2
            if self.distance > 3.0:
                self.distance = 3.0
                self.get_logger().info('Maximum distance reached: 3.0m')
        
        # Публикуем расстояние
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
