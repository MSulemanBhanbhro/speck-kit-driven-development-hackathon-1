from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """
    Generate a launch description for the integration example.

    This launch file starts the integration demo node along with supporting nodes
    to demonstrate all ROS 2 communication patterns working together.

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

    # Integration Demo Node (Lifecycle Node)
    integration_demo_node = Node(
        package='integration_example',
        executable='integration_demo',
        name='integration_demo_node',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time},
            # Example parameter overrides
            {'navigation_speed': 0.75},
            {'manipulation_precision': 0.005},
            {'safety_threshold': 0.6}
        ]
    )

    # Fibonacci Action Server (for the integration demo to use as a subordinate task)
    fibonacci_action_server_node = Node(
        package='action_server',
        executable='action_server',
        name='fibonacci_action_server',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time}
        ]
    )

    # Simple publisher for simulated sensor data
    sensor_publisher_node = Node(
        package='basic_publisher',
        executable='publisher',
        name='sensor_publisher',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time}
        ]
    )

    # Robot state publisher for visualization
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time}
        ]
    )

    return LaunchDescription([
        use_sim_time_launch_arg,
        integration_demo_node,
        fibonacci_action_server_node,
        sensor_publisher_node,
        # Note: robot_state_publisher would need a URDF parameter in real usage
        # robot_state_publisher_node
    ])