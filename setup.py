from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'exam_robot'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='student',
    maintainer_email='student@example.com',
    description='Пакет для контрольной работы по ROS 2',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'battery_node = exam_robot.battery_node:main',
            'distance_sensor = exam_robot.distance_sensor:main',
            'robot_controller = exam_robot.robot_controller:main',
            'status_display = exam_robot.status_display:main',
        ],
    },
)