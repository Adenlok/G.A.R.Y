import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, String # Int32 for sensor, String for your motor bridge

class BrainNode(Node):
    def __init__(self):
        super().__init__('robot_brain')

        # 1. Subscriber: Listen to the sensor
        self.subscription = self.create_subscription(
            Int32,
            'ultrasonic_distance', # Make sure this matches your sensor node's topic
            self.sensor_callback,
            10)

        # 2. Publisher: Talk to the Arduino Bridge
        self.motor_pub = self.create_publisher(String, 'motor_commands', 10)

        self.get_logger().info('Brain Node has started and is thinking...')

    def sensor_callback(self, msg):
        distance = msg.data
        new_command = String()

        # 3. THE BRAIN LOGIC
        if distance < 30: # If an object is closer than 30cm
            self.get_logger().warn(f'Obstacle detected at {distance}cm! Stopping.')
            new_command.data = "0,0"
        else:
            self.get_logger().info(f'Path clear ({distance}cm). Moving forward.')
            new_command.data = "500,500"

        # 4. Publish the decision
        self.motor_pub.publish(new_command)

def main(args=None):
    rclpy.init(args=args)
    node = BrainNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()