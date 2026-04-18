import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('littlebot')
    urdf_file = os.path.join(pkg_share, 'urdf', 'little_bot.urdf')
    rviz_file = os.path.join(pkg_share, 'rviz', 'config.rviz')

    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    # Đường dẫn tuyệt đối cho Gazebo tìm model path
    gazebo_models_path = os.path.join(pkg_share, '..')
    set_gazebo_model_path = SetEnvironmentVariable('GAZEBO_MODEL_PATH', gazebo_models_path)

    return LaunchDescription([
        set_gazebo_model_path,
        
        # 1. Bật Gazebo
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
            ),
            launch_arguments={'gui': 'true', 'paused': 'false'}.items() 
        ),
        
        # 2. Bật Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_desc}]
        ),
        
        # 3. Thả Robot
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'littlebot', '-topic', 'robot_description', '-z', '0.1'],
            output='screen'
        ),
        
        # 4. Bật Node Tay Máy
        Node(
            package='littlebot',
            executable='arm_controller.py',
            name='arm_controller',
            output='screen'
        ),
        
        # 5. Bật RViz kèm Config
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_file],
            output='screen'
        )
    ])