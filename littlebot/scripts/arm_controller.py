#!/usr/bin/env python3
# node dieu khien tay may tu dong di chuyen qua lai giua 2 diem Cartesian lien tuc
# su dung IK de tinh toan goc va do dai khop
import math
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

        self.joint_names = [
            'z_rail_link-v1_z_axis_joint',
            'z_slider_link-v1_arm_joint'
        ]

        # Robot params
        self.L = 0.15
        self.d_min = -0.05
        self.d_max = 0.04

        # Hai điểm Cartesian để tay máy di chuyển qua lại liên tục
        self.p0 = (0.147, -0.08)   # thu ve
        self.p1 = (0.135, 0.095)   # vuon len

        # Chuyển động liên tục: 0 -> 1 -> 0 trong motion_period giây
        self.motion_period = 4.0

        # Publish nhanh để mượt hơn
        self.publish_rate = 50.0
        self.dt = 1.0 / self.publish_rate

        # Low-pass nhẹ để giảm rung
        self.filter_gain = 0.4

        self.start_time = self.get_clock().now()
        self.current_pos = self.solve_ik(self.p0[0], self.p0[1], prev=None)

        self.timer = self.create_timer(self.dt, self.timer_callback)
        self.get_logger().info('Arm controller started')

    def clamp(self, value, low, high):
        return max(low, min(value, high))

    def solve_ik(self, target_x, target_z, prev=None):
        """
        2DOF: Prismatic d + Revolute theta
            x = L*cos(theta)
            z = d + L*sin(theta)

        Chọn nghiệm gần với trạng thái trước đó nhất để tránh nhảy nhánh IK.
        """
        x = self.clamp(target_x, -self.L, self.L)
        cos_theta = self.clamp(x / self.L, -1.0, 1.0)
        angle = math.acos(cos_theta)

        candidates = []
        for theta in (angle, -angle):
            d_raw = target_z - self.L * math.sin(theta)
            d = self.clamp(d_raw, self.d_min, self.d_max)

            # Phạt nếu vượt giới hạn prismatic
            limit_penalty = abs(d_raw - d) * 100.0

            # Ưu tiên nghiệm gần trạng thái hiện tại để chuyển động liên tục
            if prev is None:
                continuity_cost = 0.0
            else:
                continuity_cost = (
                    abs(d - prev[0]) * 8.0 +
                    abs(theta - prev[1]) * 1.0
                )

            cost = limit_penalty + continuity_cost
            candidates.append((cost, [d, theta]))

        candidates.sort(key=lambda item: item[0])
        return candidates[0][1]

    def publish_command(self, positions):
        msg = JointTrajectory()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        msg.joint_names = self.joint_names

        point = JointTrajectoryPoint()
        point.positions = positions

        point.time_from_start = Duration(sec=0, nanosec=0)

        msg.points = [point]
        self.publisher_.publish(msg)

    def timer_callback(self):
        # Thời gian chạy
        t = (self.get_clock().now() - self.start_time).nanoseconds * 1e-9

        # Hệ số mượt 0 -> 1 -> 0, vận tốc bằng 0 ở hai đầu
        s = 0.5 * (1.0 - math.cos(2.0 * math.pi * t / self.motion_period))

        # Nội suy Cartesian liên tục giữa 2 điểm
        x = self.p0[0] + (self.p1[0] - self.p0[0]) * s
        z = self.p0[1] + (self.p1[1] - self.p0[1]) * s

        target_pos = self.solve_ik(x, z, prev=self.current_pos)

        # Low-pass nhẹ để giảm rung / nhấp
        cmd = [
            self.current_pos[0] + (target_pos[0] - self.current_pos[0]) * self.filter_gain,
            self.current_pos[1] + (target_pos[1] - self.current_pos[1]) * self.filter_gain
        ]

        cmd[0] = self.clamp(cmd[0], self.d_min, self.d_max)

        self.publish_command(cmd)
        self.current_pos = cmd


def main(args=None):
    rclpy.init(args=args)
    node = ArmController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()