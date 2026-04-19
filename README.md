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
arm_controller_package/

├── arm_keyboard_teleop.py

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
chmod +x src/arm_controller_package/arm_keyboard_teleop.py
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/ros2_ws/install/littlebot/share 
```

## 5. Cách chạy
- Teleop keyboard điều khiển robot
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
- Teleop keyboard điều khiển tay may
```bash
cd /src/arm_controller_package
python3 arm_keyboard_teleop.py
```
- Launch Rviz
```bash
ros2 launch littlebot display.launch.py
```
- Launch Gazebo + Rviz
```bash
ros2 launch littlebot bringup.launch.py

```
## 6. Note
- Mặc định khi launch littlebot bringup.launch.py thì tay máy sẽ được điều khiển bằng bàn phím qua arm_keyboard_teleop.py
- Nếu muốn tay máy chạy tự động, vào ```launch/bringup.launch.py``` bỏ comment phần 4 (node điều khiển tay máy). Sau đó build lại packages littlebot là được. Lúc này bringup sẽ chạy tự động tay máy.
