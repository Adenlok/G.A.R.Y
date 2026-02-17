from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1. The micro-ROS Agent
        Node(
            package='micro_ros_agent',
            executable='micro_ros_agent',
            name='micro_ros_agent',
            arguments=['serial', '--dev', '/dev/ttyUSB1', '-b', '115200']
        ),

        # 2. THE BRAIN
        Node(
            package='robot_logic',
            executable='brain',
            name='controller'
        ),

        # 3. THE ACTUATOR
        Node(
            package='motor_control',
            executable='driver',
            name='arduino_bridge'
        )
    ])