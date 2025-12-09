#!/usr/bin/env python3
"""
Basic Publisher Example

This example demonstrates a simple publisher that sends messages to a topic.
It creates a node that publishes "Hello World" messages to the 'chatter' topic
at a rate of 2 Hz (every 0.5 seconds).
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalPublisher(Node):
    """
    A simple ROS 2 publisher node that publishes messages to a topic.
    """

    def __init__(self):
        """
        Initialize the publisher node.
        """
        super().__init__('minimal_publisher')

        # Create publisher with String message type, topic name, and queue size
        self.publisher_ = self.create_publisher(String, 'chatter', 10)

        # Create a timer to publish messages at regular intervals
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # Counter for message numbering
        self.i = 0

        # Log node creation
        self.get_logger().info('Minimal publisher node initialized')

    def timer_callback(self):
        """
        Callback function that executes when the timer fires.
        Creates and publishes a message to the 'chatter' topic.
        """
        msg = String()
        msg.data = f'Hello World: {self.i}'

        # Publish the message
        self.publisher_.publish(msg)

        # Log the published message
        self.get_logger().info(f'Publishing: "{msg.data}"')

        # Increment the counter
        self.i += 1


def main(args=None):
    """
    Main function to initialize and run the publisher node.

    Args:
        args: Command line arguments (default: None)
    """
    # Initialize the ROS 2 client library
    rclpy.init(args=args)

    # Create the publisher node
    minimal_publisher = MinimalPublisher()

    try:
        # Spin the node to process callbacks
        rclpy.spin(minimal_publisher)
    except KeyboardInterrupt:
        # Handle graceful shutdown when Ctrl+C is pressed
        pass
    finally:
        # Clean up resources
        minimal_publisher.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()