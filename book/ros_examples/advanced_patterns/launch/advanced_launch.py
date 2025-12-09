from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """
    Generate a launch description for the advanced patterns examples.

    This launch file starts multiple nodes to demonstrate advanced ROS 2 concepts
    including actions, lifecycle nodes, and parameter management.

    Returns:
        LaunchDescription: A launch description containing the nodes to launch
    """
    # Declare launch arguments
    use_sim_time_launch_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time'
    )

    # Get launch configurations
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Fibonacci Action Server node
    fibonacci_action_server_node = Node(
        package='action_server',
        executable='action_server',
        name='fibonacci_action_server',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time}
        ]
    )

    # Lifecycle Node (configured to start in unconfigured state)
    lifecycle_node = Node(
        package='advanced_patterns',
        executable='lifecycle_node',
        name='lifecycle_control_node',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time}
        ]
    )

    # Parameter Server Node
    param_server_node = Node(
        package='advanced_patterns',
        executable='param_server',
        name='parameter_server_node',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time},
            # Example: Override default parameters at launch
            {'robot_name': 'launch_robot'},
            {'control_frequency': 25},
            {'safety_threshold': 0.8},
            {'enable_logging': True}
        ]
    )

    return LaunchDescription([
        use_sim_time_launch_arg,
        fibonacci_action_server_node,
        lifecycle_node,
        param_server_node
    ])