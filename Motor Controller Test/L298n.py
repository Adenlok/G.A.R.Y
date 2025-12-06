import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import sys, termios, tty

def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch

def pack_pwm(left, right):
    # Convert to signed 16-bit mask and pack into a 32-bit int
    left16  = left & 0xFFFF
    right16 = right & 0xFFFF
    return (left16 << 16) | right16

def to_int32(x):
    x &= 0xFFFFFFFF   # force into 32-bit
    if x >= 0x80000000:
        x -= 0x100000000
    return x


def get_pwm_for_key(k):
    SPEED = 200  # change as needed (max 255)
    TURN_SPEED = 255

    if k == 'w':
        return SPEED, SPEED
    if k == 's':
        return -SPEED, -SPEED
    if k == 'a':
        # Sharp left: left reverse, right forward
        return -TURN_SPEED, TURN_SPEED
    if k == 'd':
        # Sharp right: left forward, right reverse
        return TURN_SPEED, -TURN_SPEED
    if k == ' ':
        return 0, 0
    return 0,0

class Teleop(Node):
    def __init__(self):
        super().__init__('tank_teleop')
        self.pub = self.create_publisher(Int32, 'tank_cmd', 10)
        self.get_logger().info("Tank teleop ready. Use WASD, space to stop, Ctrl-C to quit.")

def main():
    rclpy.init()
    node = Teleop()
    try:
        while True:
            ch = getch()
            pwm = get_pwm_for_key(ch)
            if pwm is None:
                continue
            left, right = pwm
            packed = pack_pwm(left, right)
            msg = Int32()
            msg.data = to_int32(packed)
            node.pub.publish(msg)
            node.get_logger().info(f"Pub L={left} R={right}")
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
