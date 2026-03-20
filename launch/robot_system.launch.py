from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Получаем путь к директории пакета
    pkg_dir = get_package_share_directory('exam_robot')
    
    # Путь к URDF файлу
    urdf_file = os.path.join(pkg_dir, 'urdf', 'exam_robot.urdf')
    
    # Читаем содержимое URDF файла
    with open(urdf_file, 'r') as f:
        robot_description = f.read()

    return LaunchDescription([
        # 1. Battery Node
        Node(
            package='exam_robot',
            executable='battery_node',
            name='battery_node',
            output='screen',
            emulate_tty=True,
            parameters=[]
        ),
        
        # 2. Distance Sensor Node
        Node(
            package='exam_robot',
            executable='distance_sensor',
            name='distance_sensor',
            output='screen',
            emulate_tty=True,
            parameters=[]
        ),
        
        # 3. Status Display Node
        Node(
            package='exam_robot',
            executable='status_display',
            name='status_display',
            output='screen',
            emulate_tty=True,
            parameters=[]
        ),
        
        # 4. Robot Controller Node
        Node(
            package='exam_robot',
            executable='robot_controller',
            name='robot_controller',
            output='screen',
            emulate_tty=True,
            parameters=[]
        ),
        
        # 5. Robot State Publisher (загружает URDF)
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            emulate_tty=True,
            parameters=[{'robot_description': robot_description}]
        ),
        
        # 6. Joint State Publisher (опционально, для публикации /joint_states)
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen',
            emulate_tty=True,
            parameters=[]
        ),
    ])
