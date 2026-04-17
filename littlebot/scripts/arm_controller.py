#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

class ArmController(Node):
    def __init__(self):
        super().__init__('arm_controller')
        self.publisher_ = self.create_publisher(
            JointTrajectory,
            '/set_joint_trajectory',
            10
        )
        self.timer = self.create_timer(4.0, self.timer_callback)
        self.toggle = True

    def timer_callback(self):
        msg = JointTrajectory()
        msg.joint_names = [
            'z_rail_link-v5_z_axis_joint',
            'z_slider_link-v5_arm_joint'
        ]

        point = JointTrajectoryPoint()

        if self.toggle:
            point.positions = [0.08, 1.0]
        else:
            point.positions = [0.0, 0.0]

        point.time_from_start = Duration(sec=2)
        msg.points.append(point)

        self.publisher_.publish(msg)
        self.get_logger().info(f'Sent target: {point.positions}')
        self.toggle = not self.toggle

def main(args=None):
    rclpy.init(args=args)
    node = ArmController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()