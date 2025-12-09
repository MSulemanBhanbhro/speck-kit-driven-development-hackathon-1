from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    """
    Generate a launch description for the joint state publisher with a humanoid robot.

    This launch file starts the joint state publisher node which allows users to set
    joint positions through a GUI and publish them to the /joint_states topic.
    This is useful for visualizing robot models with different joint configurations.

    Returns:
        LaunchDescription: A launch description containing the nodes to launch
    """
    # Declare launch arguments
    use_gui_launch_arg = DeclareLaunchArgument(
        'use_gui',
        default_value='true',
        description='Whether to use the GUI to control joint positions'
    )

    rate_launch_arg = DeclareLaunchArgument(
        'rate',
        default_value='50',
        description='Rate at which joint states are published (Hz)'
    )

    use_sim_time_launch_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time'
    )

    # Get launch configurations
    use_gui = LaunchConfiguration('use_gui')
    rate = LaunchConfiguration('rate')
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Joint State Publisher node
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time},
            {'rate': rate},
            {'use_gui': use_gui}
        ]
    )

    # If GUI is enabled, also launch the GUI node
    # Note: In most cases, the joint_state_publisher can handle GUI internally
    # but we include this as a separate option for flexibility
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time}
        ],
        condition=lambda context: LaunchConfiguration('use_gui').perform(context) == 'true'
    )

    return LaunchDescription([
        use_gui_launch_arg,
        rate_launch_arg,
        use_sim_time_launch_arg,
        joint_state_publisher_node,
        # The GUI node is only launched if use_gui is true
        joint_state_publisher_gui_node
    ])