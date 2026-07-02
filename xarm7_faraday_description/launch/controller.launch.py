#!/usr/bin/env python3
"""
ROS 2 launch file for xarm7_faraday controller manager
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    """Generate launch description for controller manager"""
    
    # Get package directories
    pkg_share = get_package_share_directory('xarm7_faraday_description')
    controller_config = os.path.join(pkg_share, 'launch', 'controller.yaml')
    urdf_file = os.path.join(pkg_share, 'urdf', 'xarm7_faraday.xacro')
    
    # Controller spawner arguments
    controllers = [
        'Revolute_1_position_controller',
        'Revolute_2_position_controller',
        'Revolute_3_position_controller',
        'Revolute_4_position_controller',
        'Revolute_5_position_controller',
        'Revolute_6_position_controller',
        'Revolute_7_position_controller',
        'joint_state_controller'
    ]
    
    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        arguments=[urdf_file],
        output='screen',
        namespace='xarm7_faraday',
        remappings=[
            ('/joint_states', '/xarm7_faraday/joint_states'),
        ]
    )
    
    # Controller manager
    control_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[controller_config],
        namespace='xarm7_faraday',
        output='screen'
    )
    
    # Controller spawner
    spawner_node = Node(
        package='controller_manager',
        executable='spawner',
        arguments=controllers,
        namespace='xarm7_faraday',
        output='screen'
    )
    
    return LaunchDescription([
        robot_state_publisher,
        control_node,
        spawner_node,
    ])
