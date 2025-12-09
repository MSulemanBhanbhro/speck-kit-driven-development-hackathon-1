#!/usr/bin/env python3
"""
Parameter Management Example

This example demonstrates a node that uses parameters for configuration.
The node declares parameters and adjusts its behavior based on parameter values.
"""

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from std_msgs.msg import String
from rcl_interfaces.msg import ParameterDescriptor, IntegerRange, ParameterType
import time


class ParametricNode(Node):
    """
    A node that demonstrates parameter management and dynamic configuration.
    """

    def __init__(self):
        """
        Initialize the parametric node.
        """
        super().__init__('parametric_node')

        # Declare parameters with descriptions and constraints
        # String parameter with description
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
            'update_rate',
            10,
            ParameterDescriptor(
                description='Update rate in Hz',
                integer_range=[IntegerRange(from_value=1, to_value=100, step=1)],
                read_only=False
            )
        )

        # Double parameter with range constraints
        self.declare_parameter(
            'safety_threshold',
            0.5,
            ParameterDescriptor(
                description='Safety threshold value',
                floating_point_range=[self._create_floating_point_range(0.0, 2.0, 0.01)],
                read_only=False
            )
        )

        # Boolean parameter
        self.declare_parameter(
            'enable_debug',
            False,
            ParameterDescriptor(
                description='Enable debug output',
                read_only=False
            )
        )

        # Get parameter values
        self.robot_name = self.get_parameter('robot_name').value
        self.update_rate = self.get_parameter('update_rate').value
        self.safety_threshold = self.get_parameter('safety_threshold').value
        self.enable_debug = self.get_parameter('enable_debug').value

        # Create publisher for status messages
        self.publisher = self.create_publisher(String, 'robot_status', 10)

        # Create timer based on update rate parameter
        timer_period = 1.0 / self.update_rate  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # Counter for messages
        self.message_count = 0

        # Log initial parameter values
        self.get_logger().info(f'Parametric node initialized with:')
        self.get_logger().info(f'  Robot name: {self.robot_name}')
        self.get_logger().info(f'  Update rate: {self.update_rate} Hz')
        self.get_logger().info(f'  Safety threshold: {self.safety_threshold}')
        self.get_logger().info(f'  Debug enabled: {self.enable_debug}')

        # Set parameter callback to handle dynamic reconfiguration
        self.set_parameters_callback(self.parameters_callback)

    def _create_floating_point_range(self, from_value, to_value, step):
        """
        Helper function to create a floating point range.

        Args:
            from_value: Minimum value
            to_value: Maximum value
            step: Step size

        Returns:
            FloatingPointRange: A floating point range object
        """
        from rcl_interfaces.msg import FloatingPointRange
        return FloatingPointRange(from_value=from_value, to_value=to_value, step=step)

    def timer_callback(self):
        """
        Callback function that executes when the timer fires.
        Publishes status messages based on current parameters.
        """
        msg = String()

        # Create status message based on parameters
        status_msg = f'Robot {self.robot_name} status: message #{self.message_count}'
        if self.enable_debug:
            status_msg += f' (threshold={self.safety_threshold})'

        msg.data = status_msg

        # Publish the message
        self.publisher.publish(msg)

        # Log the published message if debug is enabled
        if self.enable_debug:
            self.get_logger().info(f'Published: {msg.data}')

        # Increment the counter
        self.message_count += 1

    def parameters_callback(self, params):
        """
        Callback function for parameter changes.

        Args:
            params: List of Parameter objects that have changed

        Returns:
            SetParametersResult: Result indicating success or failure
        """
        from rcl_interfaces.msg import SetParametersResult

        # Process each parameter change
        for param in params:
            if param.name == 'robot_name':
                self.robot_name = param.value
                self.get_logger().info(f'Robot name updated to: {self.robot_name}')
            elif param.name == 'update_rate':
                if param.value < 1 or param.value > 100:
                    self.get_logger().error('Update rate must be between 1 and 100')
                    return SetParametersResult(successful=False, reason='Update rate out of range')
                self.update_rate = param.value
                # Update timer period
                new_period = 1.0 / self.update_rate
                self.timer.timer_period_ns = int(new_period * 1e9)
                self.get_logger().info(f'Update rate updated to: {self.update_rate} Hz')
            elif param.name == 'safety_threshold':
                if param.value < 0.0 or param.value > 2.0:
                    self.get_logger().error('Safety threshold must be between 0.0 and 2.0')
                    return SetParametersResult(successful=False, reason='Safety threshold out of range')
                self.safety_threshold = param.value
                self.get_logger().info(f'Safety threshold updated to: {self.safety_threshold}')
            elif param.name == 'enable_debug':
                self.enable_debug = param.value
                self.get_logger().info(f'Debug output {"enabled" if self.enable_debug else "disabled"}')

        # Return successful result
        return SetParametersResult(successful=True)


def main(args=None):
    """
    Main function to initialize and run the parametric node.

    Args:
        args: Command line arguments (default: None)
    """
    # Initialize the ROS 2 client library
    rclpy.init(args=args)

    # Create the parametric node
    parametric_node = ParametricNode()

    try:
        # Spin the node to process callbacks
        rclpy.spin(parametric_node)
    except KeyboardInterrupt:
        # Handle graceful shutdown when Ctrl+C is pressed
        pass
    finally:
        # Clean up resources
        parametric_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()