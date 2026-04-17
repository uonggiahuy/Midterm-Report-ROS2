# LittleBot - ROS2 Midterm Project

## 1. Mô tả
Robot littlebot là robot omnidirectional 4 bánh mecanum, có 1 trục tay máy gồm:
- 1 khớp prismatic (nâng hạ)
- 1 khớp rotation (quay tay)

Cảm biến:
- LiDAR
- IMU
- Camera

## 2. Cấu trúc package
- urdf/: mô hình robot
- meshes/: file STL
- launch/: file khởi chạy
- rviz/: cấu hình RViz
- scripts/: node điều khiển tay máy

## 3. Môi trường
- Ubuntu 24.04 - Docker container Ubuntu 22.04
- ROS2 Humble
- Gazebo
- RViz2

## 4. Cài đặt
```bash
cd ~/your_workspace/src
git clone <https://github.com/uonggiahuy/Midterm-Report-ROS2.git>
cd ..
colcon build --packages-select littlebot 
source install/setup.bash
```

## 5. Cách chạy
- Hiển thị robot trên RViz
```bash
ros2 launch littlebot display.launch.py
```
- Mở Gazebo và spawn robot
```bash
ros2 launch littlebot gazebo.launch.py
```
- Mở toàn bộ bringup
```bash
ros2 launch littlebot bringup.launch.py
```
