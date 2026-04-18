#!/usr/bin/env python3

import rclpy
from rclpy.parameter import Parameter
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import sys
import termios
import tty
import threading

msg = """
Điều khiển tay máy (Arm Controller)
---------------------------
Phím điều khiển:
        w
   a    s    d

w/s : Tăng/giảm khớp trượt tịnh tiến (Z axis)
a/d : Tăng/giảm khớp quay (Arm joint)

q   : Thoát chương trình
"""

class KeyboardArmController(Node):
    def __init__(self):
        super().__init__(
            'keyboard_arm_controller',
            parameter_overrides=[Parameter('use_sim_time', Parameter.Type.BOOL, True)]
        )
        self.publisher_ = self.create_publisher(JointTrajectory, '/set_joint_trajectory', 10)
        
        # Initial positions
        self.prismatic_pos = 0.0
        self.revolute_pos = 0.0

        # Step size
        self.prismatic_step = 0.005
        self.revolute_step = 0.05

        # Joint limits
        self.prismatic_min = -0.05
        self.prismatic_max = 0.04
        self.revolute_min = -1.0
        self.revolute_max = 0.8

        self.get_logger().info('Khởi tạo Keyboard Arm Controller')
        print(msg)

    def publish_position(self):
        traj_msg = JointTrajectory()
        traj_msg.header.stamp = self.get_clock().now().to_msg()
        traj_msg.header.frame_id = 'base_link'
        traj_msg.joint_names = ['z_rail_link-v1_z_axis_joint', 'z_slider_link-v1_arm_joint']

        point = JointTrajectoryPoint()
        point.positions = [self.prismatic_pos, self.revolute_pos]
        point.time_from_start = Duration(sec=0, nanosec=100000000) # 0.1s cho độ nhạy cao

        traj_msg.points.append(point)
        self.publisher_.publish(traj_msg)

    def update_position(self, key):
        changed = False

        if key == 'w':
            self.prismatic_pos = min(self.prismatic_pos + self.prismatic_step, self.prismatic_max)
            changed = True
        elif key == 's':
            self.prismatic_pos = max(self.prismatic_pos - self.prismatic_step, self.prismatic_min)
            changed = True
        elif key == 'd':
            self.revolute_pos = min(self.revolute_pos + self.revolute_step, self.revolute_max)
            changed = True
        elif key == 'a':
            self.revolute_pos = max(self.revolute_pos - self.revolute_step, self.revolute_min)
            changed = True

        if changed:
            # print(f"Current Pos -> Trượt: {self.prismatic_pos:.3f}, Quay: {self.revolute_pos:.3f}")
            self.publish_position()

def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def main(args=None):
    rclpy.init(args=args)
    node = KeyboardArmController()

    def spin_thread():
        rclpy.spin(node)

    thread = threading.Thread(target=spin_thread, daemon=True)
    thread.start()

    try:
        while True:
            key = get_key()
            if key == 'q' or key == '\x03': # '\x03' is Ctrl+C
                break
            node.update_position(key.lower())
    except Exception as e:
        print(e)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
