from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1. The micro-ROS Agent (Serial bridge to Ultrasonic/Motors)
        Node(
            package='micro_ros_agent',
            executable='micro_ros_agent',
            name='micro_ros_agent',
            arguments=['serial', '--dev', '/dev/ttyUSB0', '-b', '115200']
        ),

        # 2. THE TRACKER (YOLO GPU Engine)
        Node(
            package='tracking_logic',
            executable='tracker', # This matches the name in your setup.py entry_point
            name='yolo_tracker',
            output='screen'
        ),

        # 3. THE BRAIN (Control Logic)
        Node(
            package='robot_logic',
            executable='brain',
            name='controller',
            output='screen'
        ),

        # 4. THE ACTUATOR (Motor Driver)
        Node(
            package='motor_control',
            executable='driver',
            name='arduino_bridge'
        )
    ])