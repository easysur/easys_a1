import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool

class JoyToTwist(Node):

    def __init__(self):
        super().__init__('joy2cmd')

        # subscribe
        self.joy_sub = self.create_subscription(Joy, 'joy', self.joy_callback, 10)

        # publish
        self.twist_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.arm_pub = self.create_publisher(Bool, 'arm_control_command', 10)
        self.light_pub = self.create_publisher(Bool, 'light_control_command', 10)

        self.slow_gain = 0.3

        # initial control command
        self.arm_control_command = False
        self.light_control_command = False
        self._prev_arm_button = False
        self._prev_light_button = False
        self._last_arm_toggle_time = None
        self._last_light_toggle_time = None
        self._debounce_interval = Duration(seconds=0.1)  # 100 ms debounce interval

    def joy_callback(self, msg):
        twist = Twist()
        arm_command = Bool()
        light_command = Bool()

        if msg.buttons[9] == 1:
            slow_mode = False
        else:
            slow_mode = True

        now = self.get_clock().now()

        # arm
        arm_pressed = msg.buttons[1] == 1
        if arm_pressed and not self._prev_arm_button:
            if self._last_arm_toggle_time is None:
                self.arm_control_command = not self.arm_control_command
                self._last_arm_toggle_time = now
            else:
                elapsed = now - self._last_arm_toggle_time
                if elapsed.nanoseconds >= self._debounce_interval.nanoseconds:
                    self.arm_control_command = not self.arm_control_command
                    self._last_arm_toggle_time = now
        self._prev_arm_button = arm_pressed

        # light
        light_pressed = msg.buttons[3] == 1
        if light_pressed and not self._prev_light_button:
            if self._last_light_toggle_time is None:
                self.light_control_command = not self.light_control_command
                self._last_light_toggle_time = now
            else:
                elapsed = now - self._last_light_toggle_time
                if elapsed.nanoseconds >= self._debounce_interval.nanoseconds:
                    self.light_control_command = not self.light_control_command
                    self._last_light_toggle_time = now
        self._prev_light_button = light_pressed

        arm_command.data = self.arm_control_command
        light_command.data = self.light_control_command

        # twist
        twist.linear.x = msg.axes[3]
        twist.angular.z = msg.axes[0]

        # -1.0 ~ 1.0 -> 0 ~ 1
        twist.linear.z = (msg.axes[5] - 1.0) / 2.0
        if msg.buttons[10] == 1:
            twist.linear.z = -twist.linear.z

        if slow_mode == True:
            twist.linear.x = self.slow_gain*twist.linear.x
            twist.angular.z = self.slow_gain*twist.angular.z
            twist.linear.z = self.slow_gain*twist.linear.z

        # publish
        self.twist_pub.publish(twist)
        self.arm_pub.publish(arm_command)
        self.light_pub.publish(light_command)

def main(args=None):
    rclpy.init(args=args)

    node = JoyToTwist()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
