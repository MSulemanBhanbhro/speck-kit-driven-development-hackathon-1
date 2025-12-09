from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """
    Generate a launch description for the node implementation examples.

    This launch file starts multiple nodes to demonstrate different aspects
    of node implementation including sensor nodes, control servers, and parameter management.

    Returns:
        LaunchDescription: A launch description containing the nodes to launch
    """
    return LaunchDescription([
        # Launch the sensor node
        Node(
            package='node_implementation',
            executable='sensor_node',
            name='imu_sensor',
            output='screen',  # Output to screen for debugging
            parameters=[
                # Add any parameters here if needed
            ]
        ),
        # Launch the control server node
        Node(
            package='node_implementation',
            executable='control_server',
            name='robot_controller',
            output='screen',  # Output to screen for debugging
            parameters=[
                # Add any parameters here if needed
            ]
        ),
        # Launch the parametric node
        Node(
            package='node_implementation',
            executable='parametric_node',
            name='parametric_demo',
            output='screen',  # Output to screen for debugging
            parameters=[
                # Example parameters that can be overridden at launch
                {'robot_name': 'demo_robot'},
                {'update_rate': 5},
                {'safety_threshold': 0.75},
                {'enable_debug': True}
            ]
        )
    ])