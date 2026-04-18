# LittleBot - ROS2 Midterm Project - Uong Gia Huy

## 1. Mô tả
Robot littlebot là robot omnidirectional 4 bánh mecanum, có 1 trục tay máy gồm:
- 1 khớp prismatic (nâng hạ)
- 1 khớp rotation (quay tay)

Cảm biến:
- LiDAR
- IMU
- Camera

## 2. Cấu trúc package
littlebot/

├── CMakeLists.txt

├── package.xml

├── meshes/ (Chứa các file .stl của littlebot)

├── urdf/ little_bot.urdf (mô hình robot)

├── launch/ (Chứa file bringup khởi chạy Gazebo + Rviz)

├── rviz/ (Chứa file config giao diện RViz)

└── scripts/ (Chứa code Python điều khiển tay máy)

## 3. Môi trường
- Ubuntu 24.04 - Docker container Ubuntu 22.04
- ROS2 Humble
- Gazebo
- RViz2

## 4. Cài đặt
```bash
cd ~/your_workspace/src
git clone < https://github.com/uonggiahuy/Midterm-Report-ROS2.git >
cd ..
colcon build --packages-select littlebot 
source install/setup.bash
chmod +x src/littlebot/scripts/arm_controller.py
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/ros2_ws/install/littlebot/share 
```

## 5. Cách chạy
- Teleop keyboard điều khiển robot
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
- Launch Gazebo + Rviz
```bash
ros2 launch littlebot bringup.launch.py

```