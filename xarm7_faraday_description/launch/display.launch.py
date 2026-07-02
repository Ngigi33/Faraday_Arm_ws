#!/usr/bin/env python3
"""
ROS 2 launch file for displaying xarm7_faraday with RViz
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    """Generate launch description for RViz visualization"""
    
    # Get package directories
    pkg_share = get_package_share_directory('xarm7_faraday_description')
    urdf_file = os.path.join(pkg_share, 'urdf', 'xarm7_faraday.xacro')
    rviz_config = os.path.join(pkg_share, 'launch', 'urdf.rviz')
    
    # Launch arguments
    declare_gui = DeclareLaunchArgument(
        'gui',
        default_value='true',
        description='Enable GUI for joint state publisher'
    )
    
    # Joint state publisher (with GUI)
    joint_state_publisher = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen'
    )
    
    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        arguments=[urdf_file],
        output='screen'
    )
    
    # RViz
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config],
        output='screen'
    )
    
    return LaunchDescription([
        declare_gui,
        joint_state_publisher,
        robot_state_publisher,
        rviz,
    ])
