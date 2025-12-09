#!/usr/bin/env python3
"""
Action Client Example

This example demonstrates an action client that sends goals to an action server,
receives feedback during execution, and handles the final result. The client
interacts with the Fibonacci action server to compute Fibonacci sequences.
"""

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci


class FibonacciActionClient(Node):
    """
    An action client that sends Fibonacci sequence computation goals to the action server.
    """

    def __init__(self):
        """
        Initialize the Fibonacci action client.
        """
        super().__init__('fibonacci_action_client')

        # Create action client for the Fibonacci action
        self._action_client = ActionClient(
            self,
            Fibonacci,
            'fibonacci'
        )

        self.get_logger().info('Fibonacci action client initialized')

    def send_goal(self, order):
        """
        Send a goal to the Fibonacci action server.

        Args:
            order: The order of the Fibonacci sequence to compute

        Returns:
            Future object representing the asynchronous goal request
        """
        # Wait for the action server to be available
        self.get_logger().info('Waiting for action server to become available...')
        self._action_client.wait_for_server()

        # Create the goal message
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self.get_logger().info(f'Sending goal: compute Fibonacci sequence of order {order}')

        # Send the goal and register the feedback callback
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        # Add a callback for when the goal response is received
        self._send_goal_future.add_done_callback(self.goal_response_callback)

        return self._send_goal_future

    def goal_response_callback(self, future):
        """
        Callback function for when the goal response is received.

        Args:
            future: The future object for the goal request
        """
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected by server')
            return

        self.get_logger().info('Goal accepted by server')

        # Request the result future
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        """
        Callback function for receiving feedback during action execution.

        Args:
            feedback_msg: The feedback message from the action server
        """
        sequence_length = len(feedback_msg.feedback.sequence)
        current_value = feedback_msg.feedback.sequence[-1] if feedback_msg.feedback.sequence else 0

        self.get_logger().info(
            f'Received feedback: sequence length = {sequence_length}, '
            f'current value = {current_value}'
        )

    def get_result_callback(self, future):
        """
        Callback function for when the final result is received.

        Args:
            future: The future object for the result request
        """
        result = future.result().result
        sequence = result.sequence

        self.get_logger().info(f'Result received: Fibonacci sequence has {len(sequence)} numbers')
        self.get_logger().info(f'Full sequence: {sequence}')

        # Print the last few numbers of the sequence
        if len(sequence) > 5:
            self.get_logger().info(f'Last 5 numbers: {sequence[-5:]}')
        else:
            self.get_logger().info(f'Complete sequence: {sequence}')


def main(args=None):
    """
    Main function to initialize and run the Fibonacci action client.
    Sends a goal to compute the 10th Fibonacci number and waits for the result.

    Args:
        args: Command line arguments (default: None)
    """
    # Initialize the ROS 2 client library
    rclpy.init(args=args)

    # Create the action client node
    action_client = FibonacciActionClient()

    try:
        # Send a goal to compute the 10th Fibonacci number
        action_client.send_goal(10)

        # Spin to process callbacks until the result is received
        # In a real application, you might want to do other work while waiting
        rclpy.spin(action_client)
    except KeyboardInterrupt:
        # Handle graceful shutdown when Ctrl+C is pressed
        pass
    finally:
        # Clean up resources
        action_client.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()