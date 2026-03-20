from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_dir = get_package_share_directory('exam_robot')
    urdf_file = os.path.join(pkg_dir, 'urdf', 'exam_robot.urdf')
    
    with open(urdf_file, 'r') as f:
        robot_description = f.read()

    return LaunchDescription([
        # Battery node
        Node(
            package='exam_robot',
            executable='battery_node',
            name='battery_node',
            output='screen'
        ),
        
        # Distance sensor node
        Node(
            package='exam_robot',
            executable='distance_sensor',
            name='distance_sensor',
            output='screen'
        ),
        
        # Status display node
        Node(
            package='exam_robot',
            executable='status_display',
            name='status_display',
            output='screen'
        ),
        
        # Robot controller node
        Node(
            package='exam_robot',
            executable='robot_controller',
            name='robot_controller',
            output='screen'
        ),
        
        # Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description}]
        ),
        
        # Joint State Publisher (для публикации /joint_states)
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen'
        ),
    ])