#!/usr/bin/env python3
"""
Service Server Example

This example demonstrates a simple service server that provides an addition service.
It creates a node that provides a service to add two integers and return the result.
"""

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class MinimalService(Node):
    """
    A simple ROS 2 service server node that provides an addition service.
    """

    def __init__(self):
        """
        Initialize the service server node.
        """
        super().__init__('minimal_service')

        # Create service with service type, name, and callback
        self.srv = self.create_service(
            AddTwoInts,
            'add_two_ints',
            self.add_two_ints_callback
        )

        # Log node creation
        self.get_logger().info('Minimal service server initialized')

    def add_two_ints_callback(self, request, response):
        """
        Callback function that executes when a service request is received.

        Args:
            request: The service request containing two integers to add
            response: The service response to be filled with the sum

        Returns:
            The response object with the calculated sum
        """
        # Calculate the sum
        response.sum = request.a + request.b

        # Log the operation
        self.get_logger().info(f'Incoming request: {request.a} + {request.b} = {response.sum}')

        # Return the response
        return response


def main(args=None):
    """
    Main function to initialize and run the service server node.

    Args:
        args: Command line arguments (default: None)
    """
    # Initialize the ROS 2 client library
    rclpy.init(args=args)

    # Create the service server node
    minimal_service = MinimalService()

    try:
        # Spin the node to process service requests
        rclpy.spin(minimal_service)
    except KeyboardInterrupt:
        # Handle graceful shutdown when Ctrl+C is pressed
        pass
    finally:
        # Clean up resources
        minimal_service.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()