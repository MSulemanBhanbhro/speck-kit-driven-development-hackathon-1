#!/usr/bin/env python3
"""
Basic Subscriber Example

This example demonstrates a simple subscriber that receives messages from a topic.
It creates a node that subscribes to the 'chatter' topic and logs received messages.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalSubscriber(Node):
    """
    A simple ROS 2 subscriber node that receives messages from a topic.
    """

    def __init__(self):
        """
        Initialize the subscriber node.
        """
        super().__init__('minimal_subscriber')

        # Create subscription with message type, topic name, and callback
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10  # queue size
        )

        # Prevent unused variable warning
        self.subscription

        # Log node creation
        self.get_logger().info('Minimal subscriber node initialized')

    def listener_callback(self, msg):
        """
        Callback function that executes when a message is received on the topic.

        Args:
            msg: The received message of type std_msgs.msg.String
        """
        # Log the received message
        self.get_logger().info(f'I heard: "{msg.data}"')


def main(args=None):
    """
    Main function to initialize and run the subscriber node.

    Args:
        args: Command line arguments (default: None)
    """
    # Initialize the ROS 2 client library
    rclpy.init(args=args)

    # Create the subscriber node
    minimal_subscriber = MinimalSubscriber()

    try:
        # Spin the node to process callbacks
        rclpy.spin(minimal_subscriber)
    except KeyboardInterrupt:
        # Handle graceful shutdown when Ctrl+C is pressed
        pass
    finally:
        # Clean up resources
        minimal_subscriber.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()