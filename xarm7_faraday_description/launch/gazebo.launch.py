#!/usr/bin/env python3
"""
ROS 2 launch file for spawning xarm7_faraday in Gazebo
"""

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from gazebo_ros.actions import SpawnEntity

import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    """Generate launch description for Gazebo simulation"""
    
    # Get package directories
    pkg_share = get_package_share_directory('xarm7_faraday_description')
    urdf_file = os.path.join(pkg_share, 'urdf', 'xarm7_faraday.xacro')
    
    # Gazebo world file (empty by default)
    gazebo_world = LaunchConfiguration('world', default='')
    
    # Launch arguments
    declare_gazebo_world = DeclareLaunchArgument(
        'world',
        default_value='',
        description='Gazebo world file to load'
    )
    
    # Start Gazebo server
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 
                        'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': gazebo_world}.items()
    )
    
    # Load robot description from xacro
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': 'xarm7_faraday',  # Will be replaced with parsed URDF
            'use_sim_time': True,
        }],
        remappings=[
            ('/joint_states', '/xarm7_faraday/joint_states'),
        ]
    )
    
    # Spawn robot in Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'xarm7_faraday', '-file', urdf_file],
        output='screen'
    )
    
    return LaunchDescription([
        declare_gazebo_world,
        gazebo,
        robot_state_publisher,
        spawn_entity,
    ])
