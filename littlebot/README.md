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
chmod +x scripts/arm_controller.py

```

## 5. Cách chạy
- 
- Mở toàn bộ bringup
```bash
ros2 launch littlebot bringup.launch.py
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/ros2_ws/install/littlebot/share 

```