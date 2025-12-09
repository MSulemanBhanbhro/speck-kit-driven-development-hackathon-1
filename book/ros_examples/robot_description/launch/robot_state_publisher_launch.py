from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import TextSubstitution


def generate_launch_description():
    """
    Generate a launch description for the robot state publisher with a humanoid robot.

    This launch file starts the robot state publisher node with the basic humanoid URDF,
    allowing visualization of the robot model in RViz and providing TF transforms.

    Returns:
        LaunchDescription: A launch description containing the nodes to launch
    """
    # Declare launch arguments
    urdf_model_launch_arg = DeclareLaunchArgument(
        'urdf_model',
        default_value='basic_humanoid.urdf',
        description='URDF model file to load'
    )

    use_sim_time_launch_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time'
    )

    # Get launch configurations
    urdf_model = LaunchConfiguration('urdf_model')
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Get the URDF file path
    urdf_path = PathJoinSubstitution([
        FindPackageShare('robot_description'),
        'urdf',
        urdf_model
    ])

    # Robot State Publisher node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time},
            {'robot_description': PathJoinSubstitution([
                FindPackageShare('robot_description'),
                'urdf',
                urdf_model
            ])}
        ]
    )

    # Joint State Publisher node (for visualization purposes)
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time}
        ]
    )

    # Joint State Publisher GUI (optional, for manual joint control)
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time}
        ]
    )

    return LaunchDescription([
        urdf_model_launch_arg,
        use_sim_time_launch_arg,
        robot_state_publisher_node,
        joint_state_publisher_node,
        # Note: Comment out the GUI node if you don't want the interactive joint control
        # joint_state_publisher_gui_node
    ])