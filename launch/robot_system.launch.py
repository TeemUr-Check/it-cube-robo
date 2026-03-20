from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_dir = get_package_share_directory('exam_robot')
    urdf_file = os.path.join(pkg_dir, 'urdf', 'exam_robot.urdf')
    rviz_file = os.path.join(pkg_dir, 'rviz', 'exam_robot.rviz')
    
    with open(urdf_file, 'r') as f:
        robot_description = f.read()

    return LaunchDescription([
        # Battery Node с параметром
        Node(
            package='exam_robot',
            executable='battery_node',
            name='battery_node',
            output='screen',
            parameters=[{'discharge_rate': 1.0}]
        ),
        
        # Distance Sensor Node
        Node(
            package='exam_robot',
            executable='distance_sensor',
            name='distance_sensor',
            output='screen'
        ),
        
        # Status Display Node
        Node(
            package='exam_robot',
            executable='status_display',
            name='status_display',
            output='screen'
        ),
        
        # Robot Controller Node с параметром
        Node(
            package='exam_robot',
            executable='robot_controller',
            name='robot_controller',
            output='screen',
            parameters=[{'max_speed': 0.3}]
        ),
        
        # Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description}]
        ),
        
        # Joint State Publisher
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen'
        ),
        
        # RViz2
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_file],
            output='screen'
        ),
    ])
