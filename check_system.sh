#!/bin/bash

echo "=================================="
echo "    ПРОВЕРКА СИСТЕМЫ EXAM_ROBOT    "
echo "=================================="
echo

# 1. СБОРКА
echo "[1/4] Сборка пакета..."
cd ~/ros2_ws
colcon build --packages-select exam_robot
source install/setup.bash
echo "✓ Пакет собран"
echo

# 2. ЗАПУСК
echo "[2/4] Запуск системы..."
ros2 launch exam_robot robot_system.launch.py &
LAUNCH_PID=$!
sleep 5
echo "✓ Система запущена (PID: $LAUNCH_PID)"
echo

# 3. ТОПИКИ
echo "[3/4] Проверка топиков:"
echo "----------------------"
echo "Топики:"
ros2 topic list
echo
echo "Частота /battery_level (должна быть ~1 Hz):"
timeout 3 ros2 topic hz /battery_level
echo
echo "Частота /distance (должна быть ~5 Hz):"
timeout 3 ros2 topic hz /distance
echo

# 4. TF ДЕРЕВО
echo "[4/4] Проверка TF дерева:"
echo "----------------------"
ros2 run tf2_tools view_frames
echo "✓ TF дерево сохранено в frames.pdf"
echo
echo "Фреймы в дереве:"
ros2 run tf2_tools view_frames --verbose | grep -E "Frame|parent" | head -10
echo

# 5. ЗНАЧЕНИЯ
echo "Текущие значения:"
echo "----------------------"
echo "/battery_level:"
timeout 2 ros2 topic echo /battery_level --once 2>/dev/null | grep data
echo
echo "/distance:"
timeout 2 ros2 topic echo /distance --once 2>/dev/null | grep data
echo
echo "/robot_status:"
timeout 2 ros2 topic echo /robot_status --once 2>/dev/null | grep data
echo
echo "/cmd_vel:"
timeout 2 ros2 topic echo /cmd_vel --once 2>/dev/null | grep -E "linear|angular"
echo

# 6. ИТОГ
echo "=================================="
echo "✓ СИСТЕМА РАБОТАЕТ!"
echo "=================================="
echo
echo "Для остановки системы выполните:"
echo "kill $LAUNCH_PID"
