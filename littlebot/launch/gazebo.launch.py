#mở Gazebo và spawn robot.
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_path = get_package_share_directory('littlebot')
    urdf_path = os.path.join(pkg_path, 'urdf', 'little_bot.urdf')
    world_path = os.path.join(pkg_path, 'worlds', 'empty.world')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            )
        ),
        launch_arguments={'world': world_path}.items()
    )

    robot_description = ParameterValue(
        Command(['cat ', urdf_path]),
        value_type=str
    )

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
        output='screen'
    )

    spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'littlebot', '-topic', 'robot_description'],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        rsp,
        spawn
    ])