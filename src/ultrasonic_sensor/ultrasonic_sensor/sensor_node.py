import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import Jetson.GPIO as GPIO
import time

class UltrasonicNode(Node):
    def __init__(self):
        super().__init__('ultrasonic_sensor')
        self.publisher_ = self.create_publisher(Int32, 'ultrasonic_distance', 10)
        
        # Parameters for pins
        self.declare_parameter('trig_pin', 18)
        self.declare_parameter('echo_pin', 24)
        
        self.trig = self.get_parameter('trig_pin').value
        self.echo = self.get_parameter('echo_pin').value

        # GPIO Setup
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

        # Timer to read sensor at 10Hz
        self.timer = self.create_timer(0.1, self.read_distance)
        self.get_logger().info("Ultrasonic Sensor Node Started")

    def read_distance(self):
        # Trigger the pulse
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

        start_time = time.time()
        stop_time = time.time()

        # Measure the bounce back
        while GPIO.input(self.echo) == 0:
            start_time = time.time()
        while GPIO.input(self.echo) == 1:
            stop_time = time.time()

        # Calculate distance (speed of sound is 34300 cm/s)
        duration = stop_time - start_time
        distance = (duration * 34300) / 2

        # Publish
        msg = Int32()
        msg.data = int(distance)
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = UltrasonicNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
        node.destroy_node()
        rclpy.shutdown()