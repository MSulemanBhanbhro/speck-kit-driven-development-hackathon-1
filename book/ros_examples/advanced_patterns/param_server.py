#!/usr/bin/env python3
"""
Parameter Server Example

This example demonstrates a node that uses ROS 2 parameters for runtime configuration.
The node declares various types of parameters, handles dynamic reconfiguration,
and demonstrates best practices for parameter management in robotic systems.
"""

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import ParameterDescriptor, IntegerRange, FloatingPointRange, ParameterType
from std_msgs.msg import String
import time


class ParameterServerNode(Node):
    """
    A node that demonstrates comprehensive parameter management capabilities.
    """

    def __init__(self):
        """
        Initialize the parameter server node.
        """
        super().__init__('parameter_server_node')

        # Declare parameters with descriptions and constraints
        # String parameter
        self.declare_parameter(
            'robot_name',
            'default_robot',
            ParameterDescriptor(
                description='Name of the robot',
                read_only=False
            )
        )

        # Integer parameter with range constraints
        self.declare_parameter(
            'control_frequency',
            50,
            ParameterDescriptor(
                description='Control loop frequency in Hz',
                integer_range=[IntegerRange(from_value=1, to_value=1000, step=1)],
                read_only=False
            )
        )

        # Double parameter with range constraints
        self.declare_parameter(
            'safety_threshold',
            0.5,
            ParameterDescriptor(
                description='Safety threshold value for operations',
                floating_point_range=[FloatingPointRange(from_value=0.0, to_value=10.0, step=0.01)],
                read_only=False
            )
        )

        # Boolean parameter
        self.declare_parameter(
            'enable_logging',
            True,
            ParameterDescriptor(
                description='Enable detailed logging output',
                read_only=False
            )
        )

        # Array parameter (integer array)
        self.declare_parameter(
            'joint_limits',
            [90, 90, 90, 90, 90, 90],  # Example: 6 joint limits in degrees
            ParameterDescriptor(
                description='Joint position limits for each joint in degrees',
                read_only=False
            )
        )

        # Get initial parameter values
        self.robot_name = self.get_parameter('robot_name').value
        self.control_frequency = self.get_parameter('control_frequency').value
        self.safety_threshold = self.get_parameter('safety_threshold').value
        self.enable_logging = self.get_parameter('enable_logging').value
        self.joint_limits = self.get_parameter('joint_limits').value

        # Create publisher for status updates
        self.status_publisher = self.create_publisher(String, 'parameter_status', 10)

        # Create timer based on control frequency parameter
        self.update_period = 1.0 / self.control_frequency
        self.timer = self.create_timer(self.update_period, self.timer_callback)

        # Counter for messages
        self.message_count = 0

        # Log initial parameter values
        self.get_logger().info(f'Parameter server initialized with:')
        self.get_logger().info(f'  Robot name: {self.robot_name}')
        self.get_logger().info(f'  Control frequency: {self.control_frequency} Hz')
        self.get_logger().info(f'  Safety threshold: {self.safety_threshold}')
        self.get_logger().info(f'  Logging enabled: {self.enable_logging}')
        self.get_logger().info(f'  Joint limits: {self.joint_limits}')

        # Set parameter callback to handle dynamic reconfiguration
        self.set_parameters_callback(self.parameters_callback)

    def timer_callback(self):
        """
        Timer callback that executes at the control frequency.
        Publishes status messages based on current parameters.
        """
        status_msg = String()

        # Create status message based on parameters
        status = f'Robot {self.robot_name} status: msg#{self.message_count}'
        if self.enable_logging:
            status += f' (freq={self.control_frequency}Hz, threshold={self.safety_threshold})'

        status_msg.data = status

        # Publish the status message
        self.status_publisher.publish(status_msg)

        # Log the status if logging is enabled
        if self.enable_logging:
            self.get_logger().info(f'Published status: {status_msg.data}')

        # Increment the message counter
        self.message_count += 1

        # Update timer period if control frequency changed
        new_period = 1.0 / self.control_frequency
        if abs(self.timer.timer_period_ns / 1e9 - new_period) > 0.001:  # If period changed significantly
            self.timer.timer_period_ns = int(new_period * 1e9)
            self.get_logger().info(f'Timer period updated to {new_period:.3f}s ({self.control_frequency} Hz)')

    def parameters_callback(self, parameters):
        """
        Callback function for handling parameter changes.

        Args:
            parameters: List of Parameter objects that have changed

        Returns:
            SetParametersResult indicating success or failure
        """
        from rcl_interfaces.msg import SetParametersResult

        # Process each parameter change
        for param in parameters:
            if param.name == 'robot_name':
                old_name = self.robot_name
                self.robot_name = param.value
                self.get_logger().info(f'Robot name updated from "{old_name}" to "{self.robot_name}"')
            elif param.name == 'control_frequency':
                # Validate the new frequency is within acceptable range
                if param.value < 1 or param.value > 1000:
                    self.get_logger().error('Control frequency must be between 1 and 1000 Hz')
                    return SetParametersResult(successful=False, reason='Control frequency out of range')

                old_freq = self.control_frequency
                self.control_frequency = param.value
                self.get_logger().info(f'Control frequency updated from {old_freq} to {self.control_frequency} Hz')
            elif param.name == 'safety_threshold':
                # Validate the new threshold is within acceptable range
                if param.value < 0.0 or param.value > 10.0:
                    self.get_logger().error('Safety threshold must be between 0.0 and 10.0')
                    return SetParametersResult(successful=False, reason='Safety threshold out of range')

                old_threshold = self.safety_threshold
                self.safety_threshold = param.value
                self.get_logger().info(f'Safety threshold updated from {old_threshold} to {self.safety_threshold}')
            elif param.name == 'enable_logging':
                old_logging = self.enable_logging
                self.enable_logging = param.value
                status = 'enabled' if self.enable_logging else 'disabled'
                self.get_logger().info(f'Logging {status} (was {old_logging})')
            elif param.name == 'joint_limits':
                old_limits = self.joint_limits
                self.joint_limits = param.value
                self.get_logger().info(f'Joint limits updated from {old_limits} to {self.joint_limits}')

        # Return successful result
        return SetParametersResult(successful=True)

    def get_current_config(self):
        """
        Get the current configuration as a dictionary.

        Returns:
            dict: Current parameter values
        """
        return {
            'robot_name': self.robot_name,
            'control_frequency': self.control_frequency,
            'safety_threshold': self.safety_threshold,
            'enable_logging': self.enable_logging,
            'joint_limits': self.joint_limits
        }


def main(args=None):
    """
    Main function to initialize and run the parameter server node.

    Args:
        args: Command line arguments (default: None)
    """
    # Initialize the ROS 2 client library
    rclpy.init(args=args)

    # Create the parameter server node
    param_server = ParameterServerNode()

    try:
        # Print instructions for users
        param_server.get_logger().info('Parameter server running. You can change parameters using:')
        param_server.get_logger().info('  ros2 param set /parameter_server_node robot_name "new_name"')
        param_server.get_logger().info('  ros2 param set /parameter_server_node control_frequency 100')
        param_server.get_logger().info('  ros2 param set /parameter_server_node safety_threshold 0.75')
        param_server.get_logger().info('  ros2 param set /parameter_server_node enable_logging false')

        # Spin the node to process callbacks and parameter updates
        rclpy.spin(param_server)
    except KeyboardInterrupt:
        # Handle graceful shutdown when Ctrl+C is pressed
        param_server.get_logger().info('Shutting down parameter server...')
    finally:
        # Clean up resources
        param_server.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()