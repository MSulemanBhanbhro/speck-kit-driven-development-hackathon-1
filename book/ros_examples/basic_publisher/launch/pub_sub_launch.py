from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """
    Generate a launch description for the publisher and subscriber example.

    This launch file starts both the publisher and subscriber nodes simultaneously,
    allowing them to communicate through the 'chatter' topic.

    Returns:
        LaunchDescription: A launch description containing the nodes to launch
    """
    return LaunchDescription([
        # Launch the publisher node
        Node(
            package='basic_publisher',
            executable='publisher',
            name='talker',
            output='screen',  # Output to screen for debugging
            parameters=[
                # Add any parameters here if needed
            ]
        ),
        # Launch the subscriber node
        Node(
            package='basic_subscriber',
            executable='subscriber',
            name='listener',
            output='screen',  # Output to screen for debugging
            parameters=[
                # Add any parameters here if needed
            ]
        )
    ])