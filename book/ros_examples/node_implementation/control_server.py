#!/usr/bin/env python3
"""
Control Server Example

This example demonstrates a control server that responds to service calls for robot control.
The server provides services to start, stop, and set the speed of a simulated robot.
"""

import rclpy
from rclpy.node import Node
from example_interfaces.srv import SetBool, Trigger
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist


class ControlServerNode(Node):
    """
    A control server node that provides services for robot control.
    """

    def __init__(self):
        """
        Initialize the control server node.
        """
        super().__init__('control_server_node')

        # Create services for different control functions
        self.start_service = self.create_service(
            Trigger, 'start_robot', self.start_robot_callback)
        self.stop_service = self.create_service(
            Trigger, 'stop_robot', self.stop_robot_callback)
        self.set_speed_service = self.create_service(
            SetBool, 'set_robot_speed', self.set_speed_callback)

        # Create publishers for robot commands
        self.velocity_publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.speed_publisher = self.create_publisher(Float64, 'robot_speed', 10)

        # Robot state variables
        self.is_running = False
        self.current_speed = 0.0
        self.target_speed = 0.0

        # Log node creation
        self.get_logger().info('Control server node initialized with start/stop/set_speed services')

    def start_robot_callback(self, request, response):
        """
        Callback function for the start robot service.

        Args:
            request: The service request (Trigger request)
            response: The service response to be filled

        Returns:
            The response object with success status and message
        """
        try:
            if self.is_running:
                response.success = False
                response.message = "Robot is already running"
                self.get_logger().info('Start request ignored - robot already running')
            else:
                # Start the robot
                self.is_running = True
                self.current_speed = self.target_speed

                # Publish initial velocity command
                self.publish_velocity_command()

                response.success = True
                response.message = "Robot started successfully"
                self.get_logger().info('Robot started')

        except Exception as e:
            response.success = False
            response.message = f"Start failed: {str(e)}"
            self.get_logger().error(f'Start error: {str(e)}')

        return response

    def stop_robot_callback(self, request, response):
        """
        Callback function for the stop robot service.

        Args:
            request: The service request (Trigger request)
            response: The service response to be filled

        Returns:
            The response object with success status and message
        """
        try:
            if not self.is_running:
                response.success = False
                response.message = "Robot is already stopped"
                self.get_logger().info('Stop request ignored - robot already stopped')
            else:
                # Stop the robot
                self.is_running = False
                self.current_speed = 0.0
                self.target_speed = 0.0

                # Publish stop command
                self.publish_velocity_command()

                response.success = True
                response.message = "Robot stopped successfully"
                self.get_logger().info('Robot stopped')

        except Exception as e:
            response.success = False
            response.message = f"Stop failed: {str(e)}"
            self.get_logger().error(f'Stop error: {str(e)}')

        return response

    def set_speed_callback(self, request, response):
        """
        Callback function for the set robot speed service.

        Args:
            request: The service request (SetBool request with data indicating speed)
            response: The service response to be filled

        Returns:
            The response object with success status and message
        """
        try:
            # Interpret the boolean value as speed setting
            # True = high speed, False = low speed (for this example)
            if request.data:
                self.target_speed = 1.0  # High speed
                speed_description = "high speed"
            else:
                self.target_speed = 0.5  # Low speed
                speed_description = "low speed"

            # If robot is running, update current speed to target speed
            if self.is_running:
                self.current_speed = self.target_speed
                self.publish_velocity_command()

            # Publish speed update
            speed_msg = Float64()
            speed_msg.data = self.target_speed
            self.speed_publisher.publish(speed_msg)

            response.success = True
            response.message = f"Speed set to {speed_description} ({self.target_speed})"
            self.get_logger().info(f'Speed set to {speed_description}')

        except Exception as e:
            response.success = False
            response.message = f"Set speed failed: {str(e)}"
            self.get_logger().error(f'Set speed error: {str(e)}')

        return response

    def publish_velocity_command(self):
        """
        Publish a velocity command based on current robot state.
        """
        # Create and publish twist message
        twist_msg = Twist()
        if self.is_running:
            # Set linear velocity based on current speed
            twist_msg.linear.x = self.current_speed
            twist_msg.angular.z = 0.0  # No rotation for this example
        else:
            # Stop - zero velocities
            twist_msg.linear.x = 0.0
            twist_msg.angular.z = 0.0

        self.velocity_publisher.publish(twist_msg)

        self.get_logger().info(
            f'Published velocity command: linear.x={twist_msg.linear.x}, '
            f'angular.z={twist_msg.angular.z}'
        )


def main(args=None):
    """
    Main function to initialize and run the control server node.

    Args:
        args: Command line arguments (default: None)
    """
    # Initialize the ROS 2 client library
    rclpy.init(args=args)

    # Create the control server node
    control_server = ControlServerNode()

    try:
        # Spin the node to process service requests
        rclpy.spin(control_server)
    except KeyboardInterrupt:
        # Handle graceful shutdown when Ctrl+C is pressed
        pass
    finally:
        # Clean up resources
        control_server.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()