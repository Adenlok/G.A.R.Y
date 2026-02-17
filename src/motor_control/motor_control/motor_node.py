import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray, String
import serial
import time

class ArduinoBridge(Node):
    def __init__(self):
        super().__init__('arduino_bridge')
        
        # 1. Declare Parameters with Defaults
        self.declare_parameter('port', '/dev/ttyACM0')
        self.declare_parameter('baudrate', 115200)
        self.declare_parameter('loop_rate', 0.02)

        # 2. Get the values provided by the Launch file (or use defaults)
        port_name = self.get_parameter('port').value
        baud_rate = self.get_parameter('baudrate').value
        loop_rate = self.get_parameter('loop_rate').value

        # 3. Define Publishers/Subscribers
        self.subscription = self.create_subscription(
            String,
            'motor_commands',
            self.listener_callback,
            10)
        
        self.telemetry_pub = self.create_publisher(
            Int32MultiArray, 
            'motor_telemetry', 
            10)

        # 4. Setup Serial using the parameters
        try:
            self.ser = serial.Serial(port_name, baud_rate, timeout=0.05)
            self.get_logger().info(f'Connected to Arduino on {port_name} at {baud_rate}')
        except Exception as e:
            self.get_logger().error(f'Failed to connect to Serial: {e}')
            raise e # Crash the node so you know the hardware isn't connected

        # 5. Timer using the loop_rate parameter
        self.timer = self.create_timer(loop_rate, self.serial_read_callback)

    def listener_callback(self, msg):
        """Sends ROS commands to Arduino"""
        if hasattr(self, 'ser') and self.ser.is_open:
            self.ser.write(f"{msg.data}\n".encode())

    def serial_read_callback(self):
        """Reads Arduino data and publishes to ROS 2"""
        if hasattr(self, 'ser') and self.ser.in_waiting > 0:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                if line.startswith("TELEMETRY:"):
                    parts = line.split(":")[1].split(",")
                    
                    msg = Int32MultiArray()
                    msg.data = [int(p) for p in parts] # [distL, distR, speedL, speedR]
                    self.telemetry_pub.publish(msg)
            except Exception as e:
                pass

def main(args=None):
    rclpy.init(args=args)
    node = ArduinoBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()