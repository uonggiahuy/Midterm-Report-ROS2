#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

class ArmController(Node):
    def __init__(self):
        super().__init__('arm_controller')
        self.publisher_ = self.create_publisher(JointTrajectory, '/set_joint_trajectory', 10)
        self.timer = self.create_timer(4.0, self.timer_callback)
        self.toggle = True

    def timer_callback(self):
        msg = JointTrajectory()
        
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        
        msg.joint_names = ['z_rail_link-v1_z_axis_joint', 'z_slider_link-v1_arm_joint']
        point = JointTrajectoryPoint()
        
        if self.toggle:
            point.positions = [-0.03, 0.45]
            self.get_logger().info('Tay may: Vuon len')
        else:
            point.positions = [0.0, 0.0]  
            self.get_logger().info('Tay may: Thu ve')
            
        point.time_from_start = Duration(sec=2, nanosec=0)
        msg.points.append(point)
        self.publisher_.publish(msg)
        self.toggle = not self.toggle

def main(args=None):
    rclpy.init(args=args)
    node = ArmController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
