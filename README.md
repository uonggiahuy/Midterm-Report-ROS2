# LittleBot - ROS2 Midterm Project - Uong Gia Huy

## 1. Mô tả
Robot littlebot là robot omnidirectional 4 bánh mecanum, có 1 trục tay máy gồm:
- 1 khớp prismatic (nâng hạ)
- 1 khớp rotation (quay tay)

Cảm biến:
- LiDAR
- IMU
- Camera
Đây là dự án giữa kỳ của môn Lập trình Robot với ROS tại UET-VNU! 
## 2. Cấu trúc package
```bash
.
├── 📦 arm_controller_package       # Package điều khiển tay máy
│   └── 📄 arm_keyboard_teleop.py   # Node điều khiển từ bàn phím
│
└── 📦 littlebot                    # Package mô hình và cấu hình robot
    ├── 📄 CMakeLists.txt           # File cấu hình biên dịch CMake
    ├── 📄 package.xml              # Định nghĩa dependencies của package
    ├── 📁 meshes                   # Chứa các file .stl
    ├── 📁 urdf                     # Chứa file mô tả robot (LittleBot URDF)
    │   └── 📄 little_bot.urdf
    ├── 📁 launch                   # Các tệp khởi chạy hệ thống
    │   ├── 🚀 bringup.launch.py    # Khởi chạy Gazebo + RViz2 
    │   └── 🚀 display.launch.py    # Khởi chạy RViz2 + Joint State Publisher
    ├── 📁 rviz                     # Cấu hình Rviz2
    │   └── 📄 config.rviz
    ├── 📁 world                    # Chứa map Gazebo
    │   └── 📄 sample.world         # Map sample Gazebo
    └── 📁 scripts                  # Mã chạy theo kịch bản
        └── 📄 arm_controller.py    # Code Python điều khiển tay máy tự động
```
## 3. Môi trường
- Ubuntu 24.04 - Docker container Ubuntu 22.04
- ROS2 Humble
- Gazebo Classic
- RViz2

## 4. Cài đặt
- Clone Repo này về máy và build package:
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
- Cài đặt package ```teleop_twist_keyboard```
```bash
sudo apt install ros-humble-teleop-twist-keyboard -y
```
- Cần cài đặt thêm plugin imu trong Rviz (bắt buộc):
```bash
sudo apt install ros-humble-rviz-imu-plugin ros-humble-imu-tools -y
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
