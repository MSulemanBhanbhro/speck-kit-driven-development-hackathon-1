#!/usr/bin/env python3
"""
Control Client Example

This example demonstrates a control client that calls robot control services.
The client provides a simple interface to start, stop, and set the speed of a robot.
"""

import rclpy
from rclpy.node import Node
from example_interfaces.srv import SetBool, Trigger
import sys


class ControlClientNode(Node):
    """
    A control client node that calls robot control services.
    """

    def __init__(self):
        """
        Initialize the control client node.
        """
        super().__init__('control_client_node')

        # Create clients for the control services
        self.start_client = self.create_client(Trigger, 'start_robot')
        self.stop_client = self.create_client(Trigger, 'stop_robot')
        self.set_speed_client = self.create_client(SetBool, 'set_robot_speed')

        # Wait for services to be available
        self.wait_for_services()

        # Create request objects
        self.start_request = Trigger.Request()
        self.stop_request = Trigger.Request()
        self.set_speed_request = SetBool.Request()

        # Log node creation
        self.get_logger().info('Control client node initialized with service clients')

    def wait_for_services(self):
        """
        Wait for all required services to be available.
        """
        while not self.start_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Start service not available, waiting again...')

        while not self.stop_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Stop service not available, waiting again...')

        while not self.set_speed_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Set speed service not available, waiting again...')

        self.get_logger().info('All control services are available')

    def send_start_request(self):
        """
        Send a request to start the robot.

        Returns:
            The future object representing the asynchronous service call
        """
        self.get_logger().info('Sending start robot request')
        future = self.start_client.call_async(self.start_request)
        return future

    def send_stop_request(self):
        """
        Send a request to stop the robot.

        Returns:
            The future object representing the asynchronous service call
        """
        self.get_logger().info('Sending stop robot request')
        future = self.stop_client.call_async(self.stop_request)
        return future

    def send_set_speed_request(self, high_speed):
        """
        Send a request to set the robot speed.

        Args:
            high_speed: Boolean indicating whether to set high speed (True) or low speed (False)

        Returns:
            The future object representing the asynchronous service call
        """
        self.set_speed_request.data = high_speed
        speed_description = "high" if high_speed else "low"
        self.get_logger().info(f'Sending set speed request: {speed_description}')
        future = self.set_speed_client.call_async(self.set_speed_request)
        return future


def main(args=None):
    """
    Main function to initialize and run the control client node.
    Provides a command-line interface to control the robot.

    Args:
        args: Command line arguments (default: None)
    """
    # Initialize the ROS 2 client library
    rclpy.init(args=args)

    # Create the control client node
    control_client = ControlClientNode()

    # Check if command line arguments are provided
    if len(sys.argv) < 2:
        print('Usage:')
        print('  python3 control_client.py start    # Start the robot')
        print('  python3 control_client.py stop     # Stop the robot')
        print('  python3 control_client.py high     # Set high speed')
        print('  python3 control_client.py low      # Set low speed')
        sys.exit(1)

    command = sys.argv[1].lower()

    try:
        if command == 'start':
            # Send start request
            future = control_client.send_start_request()
        elif command == 'stop':
            # Send stop request
            future = control_client.send_stop_request()
        elif command == 'high':
            # Send set high speed request
            future = control_client.send_set_speed_request(True)
        elif command == 'low':
            # Send set low speed request
            future = control_client.send_set_speed_request(False)
        else:
            print(f'Unknown command: {command}')
            print('Valid commands: start, stop, high, low')
            sys.exit(1)

        # Wait for the service call to complete
        rclpy.spin_until_future_complete(control_client, future)

        # Check if the future completed successfully
        if future.done():
            response = future.result()
            if response is not None:
                if response.success:
                    print(f'Success: {response.message}')
                else:
                    print(f'Failed: {response.message}')
            else:
                print('Service call returned None response')
        else:
            print('Service call failed or timed out')

    except KeyboardInterrupt:
        print('Interrupted during service call')
    finally:
        # Clean up resources
        control_client.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()