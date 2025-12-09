#!/usr/bin/env python3
"""
Action Server Example

This example demonstrates an action server that performs a multi-step process with feedback and goal management.
The server implements a Fibonacci sequence generator as an action, which is a classic example of a long-running
operation that provides feedback during execution.
"""

import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from example_interfaces.action import Fibonacci


class FibonacciActionServer(Node):
    """
    An action server that computes Fibonacci sequences with feedback and cancellation support.
    """

    def __init__(self):
        """
        Initialize the Fibonacci action server.
        """
        super().__init__('fibonacci_action_server')

        # Create action server with the Fibonacci action type
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )

        self.get_logger().info('Fibonacci action server initialized')

    def goal_callback(self, goal_request):
        """
        Callback function for handling incoming goal requests.

        Args:
            goal_request: The incoming goal request message

        Returns:
            GoalResponse.ACCEPT or GoalResponse.REJECT
        """
        self.get_logger().info(f'Received goal request with order: {goal_request.order}')

        # Validate the goal request - reject if order is negative
        if goal_request.order < 0:
            self.get_logger().warn('Invalid order requested (negative), rejecting goal')
            return GoalResponse.REJECT

        # Accept all valid goals
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        """
        Callback function for handling goal cancellation requests.

        Args:
            goal_handle: The goal handle for the goal being cancelled

        Returns:
            CancelResponse.ACCEPT or CancelResponse.REJECT
        """
        self.get_logger().info('Received cancel request')
        # Accept all cancel requests
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        """
        Callback function for executing the action goal.

        Args:
            goal_handle: The goal handle for the executing goal

        Returns:
            The result message
        """
        self.get_logger().info('Executing Fibonacci sequence goal...')

        # Create feedback and result messages
        feedback_msg = Fibonacci.Feedback()
        result_msg = Fibonacci.Result()

        # Initialize the Fibonacci sequence
        feedback_msg.sequence = [0, 1]

        # Handle special cases where order is 0 or 1
        if goal_handle.request.order <= 1:
            if goal_handle.request.order == 0:
                result_msg.sequence = [0]
            else:
                result_msg.sequence = [0, 1]

            # Complete the goal successfully
            goal_handle.succeed()
            self.get_logger().info('Goal completed successfully for order <= 1')
            return result_msg

        # Generate the Fibonacci sequence up to the requested order
        for i in range(1, goal_handle.request.order):
            # Check if the goal has been cancelled
            if goal_handle.is_cancel_requested:
                self.get_logger().info('Goal cancelled during execution')
                result_msg.sequence = feedback_msg.sequence
                goal_handle.canceled()
                return result_msg

            # Compute the next number in the sequence
            next_num = feedback_msg.sequence[i] + feedback_msg.sequence[i-1]
            feedback_msg.sequence.append(next_num)

            # Publish feedback to let the client know about progress
            goal_handle.publish_feedback(feedback_msg)

            # Log progress periodically
            if len(feedback_msg.sequence) % 5 == 0:  # Log every 5 numbers
                self.get_logger().info(
                    f'Generated {len(feedback_msg.sequence)} Fibonacci numbers, '
                    f'current value: {next_num}'
                )

            # Simulate processing time (in a real application, this would be actual computation)
            # For this example, we'll use a small delay to demonstrate the long-running nature
            from time import sleep
            sleep(0.1)

        # Complete the goal successfully
        goal_handle.succeed()
        result_msg.sequence = feedback_msg.sequence

        self.get_logger().info(
            f'Goal completed successfully. Generated sequence with {len(result_msg.sequence)} numbers.'
        )
        return result_msg


def main(args=None):
    """
    Main function to initialize and run the Fibonacci action server.

    Args:
        args: Command line arguments (default: None)
    """
    # Initialize the ROS 2 client library
    rclpy.init(args=args)

    # Create the action server node
    action_server = FibonacciActionServer()

    try:
        # Spin the node to process action requests
        rclpy.spin(action_server)
    except KeyboardInterrupt:
        # Handle graceful shutdown when Ctrl+C is pressed
        pass
    finally:
        # Clean up resources
        action_server.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()