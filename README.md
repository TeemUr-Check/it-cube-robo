# Exam Robot

Пакет для контрольной работы по ROS 2, моделирующий систему робота с датчиками.

## Запуск

```bash
# Сборка пакета
cd ~/ros2_ws
colcon build --packages-select exam_robot
source install/setup.bash

# Запуск системы
ros2 launch exam_robot robot_system.launch.py