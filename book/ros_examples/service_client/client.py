#!/usr/bin/env python3
"""
Service Client Example

This example demonstrates a simple service client that calls the addition service.
It creates a node that sends requests to the 'add_two_ints' service and receives responses.
"""

import sys
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class MinimalClient(Node):
    """
    A simple ROS 2 service client node that calls an addition service.
    """

    def __init__(self):
        """
        Initialize the service client node.
        """
        super().__init__('minimal_client')

        # Create client for the service
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')

        # Wait for the service to be available
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')

        # Create request object
        self.request = AddTwoInts.Request()

    def send_request(self, a, b):
        """
        Send a request to the service server.

        Args:
            a: First integer to add
            b: Second integer to add

        Returns:
            The future object representing the asynchronous service call
        """
        # Set the request parameters
        self.request.a = a
        self.request.b = b

        # Make asynchronous service call
        self.future = self.cli.call_async(self.request)

        # Log the request
        self.get_logger().info(f'Sending request: {a} + {b}')

        return self.future


def main(args=None):
    """
    Main function to initialize and run the service client node.
    Sends a request to the service server and waits for the response.

    Args:
        args: Command line arguments (default: None)
    """
    # Initialize the ROS 2 client library
    rclpy.init(args=args)

    # Create the service client node
    minimal_client = MinimalClient()

    # Check if command line arguments are provided
    if len(sys.argv) != 3:
        print('Usage: python3 client.py <int1> <int2>')
        sys.exit(1)

    try:
        # Parse command line arguments
        a = int(sys.argv[1])
        b = int(sys.argv[2])
    except ValueError:
        print('Please provide two integers as arguments')
        sys.exit(1)

    # Send the request
    future = minimal_client.send_request(a, b)

    try:
        # Spin until the future is complete
        rclpy.spin_until_future_complete(minimal_client, future)

        # Check if the future completed successfully
        if future.done():
            response = future.result()
            print(f'Result: {a} + {b} = {response.sum}')
        else:
            print('Service call failed')

    except KeyboardInterrupt:
        print('Interrupted during service call')
    finally:
        # Clean up resources
        minimal_client.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()