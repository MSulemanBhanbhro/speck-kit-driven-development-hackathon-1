#!/usr/bin/env python3
"""
Integration Demo Example

This example demonstrates the integration of all concepts learned in Module 1:
- Topics (publisher/subscriber)
- Services (server/client)
- Actions (server/client)
- Parameters (dynamic reconfiguration)
- Lifecycle nodes (state management)

This comprehensive example shows how all ROS 2 communication patterns work together
in a realistic robotic scenario involving a mobile manipulator robot.
"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient, ActionServer
from rclpy.lifecycle import LifecycleNode, LifecycleState, TransitionCallbackReturn
from rclpy.parameter import Parameter
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

from std_msgs.msg import String, Float64
from sensor_msgs.msg import LaserScan, JointState
from geometry_msgs.msg import Twist
from example_interfaces.srv import SetBool, Trigger
from example_interfaces.action import Fibonacci
from rcl_interfaces.msg import ParameterDescriptor


class IntegrationDemoNode(LifecycleNode):
    """
    A comprehensive integration demo node that combines all ROS 2 communication patterns.
    Simulates a mobile manipulator robot performing a complex task.
    """

    def __init__(self):
        """
        Initialize the integration demo node in the unconfigured state.
        """
        super().__init__('integration_demo_node')

        # Initialize state tracking
        self._is_initialized = False
        self._active_resources = []
        self._robot_state = 'idle'  # idle, navigating, manipulating, etc.

        # Initialize parameters
        self.declare_parameter(
            'navigation_speed',
            0.5,
            ParameterDescriptor(description='Navigation speed in m/s')
        )
        self.declare_parameter(
            'manipulation_precision',
            0.01,
            ParameterDescriptor(description='Manipulation precision in meters')
        )
        self.declare_parameter(
            'safety_threshold',
            0.5,
            ParameterDescriptor(description='Safety distance threshold in meters')
        )

        self.get_logger().info('Integration demo node initialized in unconfigured state')

    def on_configure(self, state):
        """
        Configure the integration demo node and initialize all communication interfaces.
        """
        self.get_logger().info('Configuring integration demo node')

        try:
            # Initialize parameters
            self.navigation_speed = self.get_parameter('navigation_speed').value
            self.manipulation_precision = self.get_parameter('manipulation_precision').value
            self.safety_threshold = self.get_parameter('safety_threshold').value

            # Create publishers for robot control
            qos_profile = QoSProfile(
                depth=10,
                reliability=ReliabilityPolicy.RELIABLE,
                durability=DurabilityPolicy.VOLATILE
            )
            self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', qos_profile)
            self.joint_cmd_publisher = self.create_publisher(JointState, 'joint_commands', qos_profile)
            self.status_publisher = self.create_publisher(String, 'robot_status', qos_profile)

            # Create subscribers for sensor data
            self.laser_subscriber = self.create_subscription(
                LaserScan, 'scan', self.laser_callback, qos_profile
            )
            self.joint_state_subscriber = self.create_subscription(
                JointState, 'joint_states', self.joint_state_callback, qos_profile
            )

            # Create service server for robot control commands
            self.start_service = self.create_service(
                Trigger, 'start_robot', self.start_robot_callback
            )
            self.stop_service = self.create_service(
                Trigger, 'stop_robot', self.stop_robot_callback
            )
            self.emergency_stop_service = self.create_service(
                SetBool, 'emergency_stop', self.emergency_stop_callback
            )

            # Create action server for complex tasks
            self.navigation_action_server = ActionServer(
                self,
                Fibonacci,  # Using Fibonacci as an example - in real use, would be NavigateToPose
                'execute_task',
                execute_callback=self.execute_task_callback,
                goal_callback=self.task_goal_callback,
                cancel_callback=self.task_cancel_callback
            )

            # Create action client for subordinate tasks
            self.fibonacci_action_client = ActionClient(
                self, Fibonacci, 'fibonacci'
            )

            # Create timer for periodic status updates
            self.status_timer = self.create_timer(1.0, self.status_timer_callback)
            self.status_timer.cancel()  # Don't start yet

            # Add resources to tracking list
            self._active_resources.extend([
                self.cmd_vel_publisher, self.joint_cmd_publisher, self.status_publisher,
                self.laser_subscriber, self.joint_state_subscriber,
                self.start_service, self.stop_service, self.emergency_stop_service,
                self.navigation_action_server,
                self.status_timer
            ])

            # Set parameter callback
            self.set_parameters_callback(self.parameters_callback)

            self._is_initialized = True
            self._publish_status('CONFIGURED')

            self.get_logger().info('Integration demo node configured successfully')
            return TransitionCallbackReturn.SUCCESS

        except Exception as e:
            self.get_logger().error(f'Failed to configure integration demo node: {e}')
            return TransitionCallbackReturn.FAILURE

    def on_activate(self, state):
        """
        Activate the integration demo node and start all interfaces.
        """
        self.get_logger().info('Activating integration demo node')

        try:
            if not self._is_initialized:
                self.get_logger().error('Node not properly initialized')
                return TransitionCallbackReturn.FAILURE

            # Activate publishers
            self.cmd_vel_publisher.on_activate()
            self.joint_cmd_publisher.on_activate()
            self.status_publisher.on_activate()

            # Start status timer
            self.status_timer.reset()

            self._robot_state = 'idle'
            self._publish_status('ACTIVE')

            self.get_logger().info('Integration demo node activated successfully')
            return TransitionCallbackReturn.SUCCESS

        except Exception as e:
            self.get_logger().error(f'Failed to activate integration demo node: {e}')
            return TransitionCallbackReturn.FAILURE

    def on_deactivate(self, state):
        """
        Deactivate the integration demo node and stop active operations.
        """
        self.get_logger().info('Deactivating integration demo node')

        try:
            # Deactivate publishers
            self.cmd_vel_publisher.on_deactivate()
            self.joint_cmd_publisher.on_deactivate()
            self.status_publisher.on_deactivate()

            # Stop timer
            self.status_timer.cancel()

            self._robot_state = 'inactive'
            self._publish_status('INACTIVE')

            self.get_logger().info('Integration demo node deactivated successfully')
            return TransitionCallbackReturn.SUCCESS

        except Exception as e:
            self.get_logger().error(f'Failed to deactivate integration demo node: {e}')
            return TransitionCallbackReturn.FAILURE

    def on_cleanup(self, state):
        """
        Clean up resources when transitioning to unconfigured state.
        """
        self.get_logger().info('Cleaning up integration demo node')

        try:
            # Clean up all resources
            for resource in self._active_resources:
                if hasattr(resource, 'destroy') and callable(resource.destroy):
                    resource.destroy()

            self._active_resources.clear()
            self._is_initialized = False

            self._publish_status('CLEANED_UP')

            self.get_logger().info('Integration demo node cleaned up successfully')
            return TransitionCallbackReturn.SUCCESS

        except Exception as e:
            self.get_logger().error(f'Failed to clean up integration demo node: {e}')
            return TransitionCallbackReturn.FAILURE

    def laser_callback(self, msg):
        """
        Callback for laser scan data.

        Args:
            msg: LaserScan message with distance readings
        """
        # Check for obstacles based on safety threshold
        if min(msg.ranges) < self.safety_threshold:
            self.get_logger().warn(f'Obstacle detected at {min(msg.ranges):.2f}m, below threshold {self.safety_threshold}m')
            # In a real system, this might trigger obstacle avoidance

    def joint_state_callback(self, msg):
        """
        Callback for joint state data.

        Args:
            msg: JointState message with current joint positions
        """
        # Process joint state information
        self.get_logger().debug(f'Received joint state with {len(msg.position)} joints')

    def start_robot_callback(self, request, response):
        """
        Service callback to start robot operations.

        Args:
            request: Trigger service request
            response: Trigger service response to fill

        Returns:
            Service response with success status
        """
        try:
            if self._robot_state in ['idle', 'stopped']:
                self._robot_state = 'active'
                response.success = True
                response.message = 'Robot started successfully'
                self.get_logger().info('Robot started')
            else:
                response.success = False
                response.message = f'Robot already in state: {self._robot_state}'
                self.get_logger().info(f'Robot start rejected: already {self._robot_state}')

        except Exception as e:
            response.success = False
            response.message = f'Start failed: {str(e)}'
            self.get_logger().error(f'Start robot error: {str(e)}')

        return response

    def stop_robot_callback(self, request, response):
        """
        Service callback to stop robot operations.

        Args:
            request: Trigger service request
            response: Trigger service response to fill

        Returns:
            Service response with success status
        """
        try:
            if self._robot_state in ['active', 'navigating', 'manipulating']:
                self._robot_state = 'stopped'
                # Stop robot movement
                self._stop_robot_motion()
                response.success = True
                response.message = 'Robot stopped successfully'
                self.get_logger().info('Robot stopped')
            else:
                response.success = False
                response.message = f'Robot not in stoppable state: {self._robot_state}'
                self.get_logger().info(f'Robot stop rejected: state is {self._robot_state}')

        except Exception as e:
            response.success = False
            response.message = f'Stop failed: {str(e)}'
            self.get_logger().error(f'Stop robot error: {str(e)}')

        return response

    def emergency_stop_callback(self, request, response):
        """
        Service callback for emergency stop.

        Args:
            request: SetBool service request with data field
            response: SetBool service response to fill

        Returns:
            Service response with success status
        """
        try:
            if request.data:  # Emergency stop requested
                self._robot_state = 'emergency_stopped'
                self._stop_robot_motion()
                response.success = True
                response.message = 'Emergency stop activated'
                self.get_logger().warn('EMERGENCY STOP ACTIVATED')
            else:  # Emergency stop release
                if self._robot_state == 'emergency_stopped':
                    self._robot_state = 'idle'
                    response.success = True
                    response.message = 'Emergency stop released'
                    self.get_logger().info('Emergency stop released')
                else:
                    response.success = False
                    response.message = 'Emergency stop not active'
                    self.get_logger().info('Emergency stop release ignored - not active')

        except Exception as e:
            response.success = False
            response.message = f'Emergency stop failed: {str(e)}'
            self.get_logger().error(f'Emergency stop error: {str(e)}')

        return response

    def task_goal_callback(self, goal_request):
        """
        Callback for task goal requests.

        Args:
            goal_request: The incoming goal request

        Returns:
            GoalResponse.ACCEPT or GoalResponse.REJECT
        """
        self.get_logger().info(f'Received task goal: compute Fibonacci sequence of order {goal_request.order}')

        # Accept all goals for this example
        return rclpy.action.server.GoalResponse.ACCEPT

    def task_cancel_callback(self, goal_handle):
        """
        Callback for task cancellation requests.

        Args:
            goal_handle: The goal handle for the goal being cancelled

        Returns:
            CancelResponse.ACCEPT or CancelResponse.REJECT
        """
        self.get_logger().info('Received task cancellation request')
        return rclpy.action.server.CancelResponse.ACCEPT

    def execute_task_callback(self, goal_handle):
        """
        Execute a complex task that might involve multiple subtasks.

        Args:
            goal_handle: The goal handle for the executing goal

        Returns:
            The result message
        """
        self.get_logger().info('Executing complex integration task...')

        # Create feedback and result messages
        feedback_msg = Fibonacci.Feedback()
        result_msg = Fibonacci.Result()

        # This is a simplified example - in a real system, this might:
        # 1. Navigate to a location using topics
        # 2. Perform manipulation using services
        # 3. Execute long-running operations using actions
        # 4. Adjust parameters dynamically

        # For this example, we'll simulate a complex task using the Fibonacci sequence
        # as a placeholder for a computationally intensive operation
        feedback_msg.sequence = [0, 1]

        if goal_handle.request.order <= 1:
            if goal_handle.request.order == 0:
                result_msg.sequence = [0]
            else:
                result_msg.sequence = [0, 1]
        else:
            for i in range(1, goal_handle.request.order):
                # Check if the goal has been cancelled
                if goal_handle.is_cancel_requested:
                    self.get_logger().info('Task cancelled during execution')
                    result_msg.sequence = feedback_msg.sequence
                    goal_handle.canceled()
                    return result_msg

                # Compute the next number in the sequence
                next_num = feedback_msg.sequence[i] + feedback_msg.sequence[i-1]
                feedback_msg.sequence.append(next_num)

                # Publish feedback
                goal_handle.publish_feedback(feedback_msg)

                # Simulate processing time
                from time import sleep
                sleep(0.1)

        # Complete the task successfully
        goal_handle.succeed()
        result_msg.sequence = feedback_msg.sequence

        self.get_logger().info('Complex integration task completed successfully')
        return result_msg

    def parameters_callback(self, parameters):
        """
        Handle parameter changes dynamically.

        Args:
            parameters: List of Parameter objects that have changed

        Returns:
            SetParametersResult indicating success or failure
        """
        from rcl_interfaces.msg import SetParametersResult

        for param in parameters:
            if param.name == 'navigation_speed':
                old_speed = self.navigation_speed
                self.navigation_speed = param.value
                self.get_logger().info(f'Navigation speed updated from {old_speed} to {self.navigation_speed}')
            elif param.name == 'manipulation_precision':
                old_precision = self.manipulation_precision
                self.manipulation_precision = param.value
                self.get_logger().info(f'Manipulation precision updated from {old_precision} to {self.manipulation_precision}')
            elif param.name == 'safety_threshold':
                old_threshold = self.safety_threshold
                self.safety_threshold = param.value
                self.get_logger().info(f'Safety threshold updated from {old_threshold} to {self.safety_threshold}')

        return SetParametersResult(successful=True)

    def status_timer_callback(self):
        """
        Timer callback for periodic status updates.
        """
        status_msg = String()
        status_msg.data = f'Robot state: {self._robot_state}, speed: {self.navigation_speed}, precision: {self.manipulation_precision}'
        self.status_publisher.publish(status_msg)

    def _stop_robot_motion(self):
        """
        Helper method to stop all robot motion.
        """
        # Send zero velocity command
        stop_cmd = Twist()
        stop_cmd.linear.x = 0.0
        stop_cmd.linear.y = 0.0
        stop_cmd.linear.z = 0.0
        stop_cmd.angular.x = 0.0
        stop_cmd.angular.y = 0.0
        stop_cmd.angular.z = 0.0
        self.cmd_vel_publisher.publish(stop_cmd)

        self.get_logger().info('Robot motion stopped')

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
    Main function to initialize and run the integration demo node.

    Args:
        args: Command line arguments (default: None)
    """
    # Initialize the ROS 2 client library
    rclpy.init(args=args)

    # Create the integration demo node
    integration_node = IntegrationDemoNode()

    try:
        # Print instructions for users
        integration_node.get_logger().info('Integration demo node running. Demonstrates:')
        integration_node.get_logger().info('  - Topic communication (publishers/subscribers)')
        integration_node.get_logger().info('  - Service communication (servers/clients)')
        integration_node.get_logger().info('  - Action communication (servers/clients)')
        integration_node.get_logger().info('  - Parameter management (dynamic reconfiguration)')
        integration_node.get_logger().info('  - Lifecycle management (state transitions)')

        # Spin the node to process all communication patterns
        rclpy.spin(integration_node)
    except KeyboardInterrupt:
        # Handle graceful shutdown when Ctrl+C is pressed
        integration_node.get_logger().info('Shutting down integration demo node...')
    finally:
        # Clean up resources
        integration_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()