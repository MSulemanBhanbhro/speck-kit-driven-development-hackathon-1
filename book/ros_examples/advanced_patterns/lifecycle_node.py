#!/usr/bin/env python3
"""
Lifecycle Node Example

This example demonstrates a lifecycle node that follows the ROS 2 lifecycle state machine.
The node implements proper state transitions for configuration, activation, deactivation,
and cleanup, providing a robust foundation for complex robotic systems that need
structured initialization and resource management.
"""

import rclpy
from rclpy.lifecycle import LifecycleNode, LifecycleState, TransitionCallbackReturn
from rclpy.lifecycle import Node as rclpy_Node
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
import threading
import time


class LifecycleControlNode(LifecycleNode):
    """
    A lifecycle node that demonstrates proper state management and resource handling.
    """

    def __init__(self):
        """
        Initialize the lifecycle node in the unconfigured state.
        """
        super().__init__('lifecycle_control_node')
        self.get_logger().info('Lifecycle node initialized in unconfigured state')

        # Initialize state tracking
        self._is_initialized = False
        self._active_resources = []

    def on_configure(self, state):
        """
        Callback for the configure transition.

        Args:
            state: The current state before transition

        Returns:
            TransitionCallbackReturn.SUCCESS or TransitionCallbackReturn.FAILURE
        """
        self.get_logger().info(f'Configuring node: {self.get_name()}')

        try:
            # Initialize resources that don't require active communication
            # Create publishers and subscribers but don't activate them yet
            self.status_publisher = self.create_publisher(String, 'lifecycle_status', 10)
            self.scan_publisher = self.create_publisher(LaserScan, 'lifecycle_scan', 10)

            # Create a timer but don't start it yet
            self.timer = self.create_timer(1.0, self.timer_callback)
            self.timer.cancel()  # Don't start timer yet

            # Add resources to tracking list
            self._active_resources.extend([self.status_publisher, self.scan_publisher, self.timer])

            # Mark as initialized
            self._is_initialized = True

            # Publish status
            self._publish_status('CONFIGURED')

            self.get_logger().info('Node configured successfully')
            return TransitionCallbackReturn.SUCCESS

        except Exception as e:
            self.get_logger().error(f'Failed to configure node: {e}')
            return TransitionCallbackReturn.FAILURE

    def on_cleanup(self, state):
        """
        Callback for the cleanup transition.

        Args:
            state: The current state before transition

        Returns:
            TransitionCallbackReturn.SUCCESS or TransitionCallbackReturn.FAILURE
        """
        self.get_logger().info(f'Cleaning up node: {self.get_name()}')

        try:
            # Clean up resources created during configuration
            for resource in self._active_resources:
                if hasattr(resource, 'destroy') and callable(resource.destroy):
                    resource.destroy()

            # Clear the resources list
            self._active_resources.clear()

            # Reset initialization flag
            self._is_initialized = False

            # Publish status
            self._publish_status('CLEANED_UP')

            self.get_logger().info('Node cleaned up successfully')
            return TransitionCallbackReturn.SUCCESS

        except Exception as e:
            self.get_logger().error(f'Failed to clean up node: {e}')
            return TransitionCallbackReturn.FAILURE

    def on_activate(self, state):
        """
        Callback for the activate transition.

        Args:
            state: The current state before transition

        Returns:
            TransitionCallbackReturn.SUCCESS or TransitionCallbackReturn.FAILURE
        """
        self.get_logger().info(f'Activating node: {self.get_name()}')

        try:
            # Validate that configuration was successful
            if not self._is_initialized:
                self.get_logger().error('Node not properly initialized')
                return TransitionCallbackReturn.FAILURE

            # Activate publishers
            self.status_publisher.on_activate()
            self.scan_publisher.on_activate()

            # Start timer
            self.timer.reset()

            # Publish status
            self._publish_status('ACTIVE')

            self.get_logger().info('Node activated successfully')
            return TransitionCallbackReturn.SUCCESS

        except Exception as e:
            self.get_logger().error(f'Failed to activate node: {e}')
            return TransitionCallbackReturn.FAILURE

    def on_deactivate(self, state):
        """
        Callback for the deactivate transition.

        Args:
            state: The current state before transition

        Returns:
            TransitionCallbackReturn.SUCCESS or TransitionCallbackReturn.FAILURE
        """
        self.get_logger().info(f'Deactivating node: {self.get_name()}')

        try:
            # Deactivate publishers
            self.status_publisher.on_deactivate()
            self.scan_publisher.on_deactivate()

            # Stop timer
            self.timer.cancel()

            # Publish status
            self._publish_status('INACTIVE')

            self.get_logger().info('Node deactivated successfully')
            return TransitionCallbackReturn.SUCCESS

        except Exception as e:
            self.get_logger().error(f'Failed to deactivate node: {e}')
            return TransitionCallbackReturn.FAILURE

    def on_shutdown(self, state):
        """
        Callback for the shutdown transition.

        Args:
            state: The current state before transition

        Returns:
            TransitionCallbackReturn.SUCCESS or TransitionCallbackReturn.FAILURE
        """
        self.get_logger().info(f'Shutting down node: {self.get_name()}')

        try:
            # Perform final cleanup - this is similar to cleanup but for shutdown
            for resource in self._active_resources:
                if hasattr(resource, 'destroy') and callable(resource.destroy):
                    resource.destroy()

            # Clear the resources list
            self._active_resources.clear()

            # Publish status
            self._publish_status('SHUTDOWN')

            self.get_logger().info('Node shutdown successfully')
            return TransitionCallbackReturn.SUCCESS

        except Exception as e:
            self.get_logger().error(f'Failed during shutdown: {e}')
            return TransitionCallbackReturn.FAILURE

    def on_error(self, state):
        """
        Callback for the error transition.

        Args:
            state: The current state before transition

        Returns:
            TransitionCallbackReturn.SUCCESS or TransitionCallbackReturn.FAILURE
        """
        self.get_logger().error(f'Error occurred in node: {self.get_name()}')
        # Publish error status
        self._publish_status('ERROR')
        # Return SUCCESS to allow transition to error state
        return TransitionCallbackReturn.SUCCESS

    def timer_callback(self):
        """
        Timer callback that only executes when node is active.
        This simulates periodic work that should only happen when the node is active.
        """
        # Create and publish a status message
        status_msg = String()
        status_msg.data = f'Node active at: {self.get_clock().now().nanoseconds}'
        self.status_publisher.publish(status_msg)

        # Create and publish a simulated laser scan
        scan_msg = LaserScan()
        scan_msg.header.stamp = self.get_clock().now().to_msg()
        scan_msg.header.frame_id = 'laser_frame'
        scan_msg.angle_min = -1.57  # -90 degrees
        scan_msg.angle_max = 1.57   # 90 degrees
        scan_msg.angle_increment = 0.01
        scan_msg.time_increment = 0.0
        scan_msg.scan_time = 0.0
        scan_msg.range_min = 0.1
        scan_msg.range_max = 10.0
        scan_msg.ranges = [1.0 + (i * 0.01) for i in range(315)]  # 315 range values

        self.scan_publisher.publish(scan_msg)

        self.get_logger().info(f'Timer callback executed: published status and scan data')

    def _publish_status(self, status):
        """
        Helper method to publish node status.

        Args:
            status: The status string to publish
        """
        if hasattr(self, 'status_publisher'):
            status_msg = String()
            status_msg.data = f'{self.get_name()}: {status}'
            self.status_publisher.publish(status_msg)


def main(args=None):
    """
    Main function to initialize and run the lifecycle node.

    Args:
        args: Command line arguments (default: None)
    """
    # Initialize the ROS 2 client library
    rclpy.init(args=args)

    # Create the lifecycle node
    lifecycle_node = LifecycleControlNode()

    try:
        # Spin the node to process callbacks
        # In a real application, you would typically use a lifecycle manager
        # to control the node's state transitions
        rclpy.spin(lifecycle_node)
    except KeyboardInterrupt:
        # Handle graceful shutdown when Ctrl+C is pressed
        pass
    finally:
        # Clean up resources
        lifecycle_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()