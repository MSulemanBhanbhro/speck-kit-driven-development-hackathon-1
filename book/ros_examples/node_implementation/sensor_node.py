#!/usr/bin/env python3
"""
Sensor Node Example

This example demonstrates a sensor node that publishes sensor data and responds to service calls.
The node simulates an IMU (Inertial Measurement Unit) sensor that publishes data at 50 Hz
and provides a service to calibrate the sensor.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from std_msgs.msg import Header
from example_interfaces.srv import Trigger
import math
import time


class SensorNode(Node):
    """
    A sensor node that publishes IMU data and provides calibration service.
    """

    def __init__(self):
        """
        Initialize the sensor node.
        """
        super().__init__('sensor_node')

        # Create publisher for IMU data
        self.publisher = self.create_publisher(Imu, 'imu_data', 10)

        # Create timer to publish sensor data at 50 Hz
        self.timer = self.create_timer(0.02, self.publish_imu_data)  # 50 Hz (0.02 seconds)

        # Create service for sensor calibration
        self.calibration_service = self.create_service(
            Trigger, 'calibrate_sensor', self.calibrate_sensor_callback)

        # Initialize sensor data
        self.sequence_number = 0
        self.start_time = time.time()
        self.calibration_offset = 0.0

        # Log node creation
        self.get_logger().info('Sensor node initialized with IMU publisher and calibration service')

    def publish_imu_data(self):
        """
        Publish simulated IMU data to the 'imu_data' topic.
        """
        msg = Imu()

        # Set header
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'imu_link'
        msg.header.seq = self.sequence_number

        # Simulate sensor data with time-varying components
        current_time = time.time() - self.start_time

        # Set orientation (simulated with small oscillations)
        msg.orientation.x = 0.0
        msg.orientation.y = 0.0
        msg.orientation.z = math.sin(current_time * 0.5) * 0.1 + self.calibration_offset
        msg.orientation.w = math.cos(current_time * 0.5) * 0.1

        # Set orientation covariance (unknown)
        msg.orientation_covariance = [-1.0] + [0.0] * 8

        # Set angular velocity (simulated)
        msg.angular_velocity.x = math.cos(current_time) * 0.01
        msg.angular_velocity.y = math.sin(current_time) * 0.01
        msg.angular_velocity.z = 0.01

        # Set angular velocity covariance (unknown)
        msg.angular_velocity_covariance = [0.0] * 9

        # Set linear acceleration (simulated with gravity component)
        msg.linear_acceleration.x = math.sin(current_time * 2) * 0.5
        msg.linear_acceleration.y = math.cos(current_time * 2) * 0.3
        msg.linear_acceleration.z = 9.81  # gravity

        # Set linear acceleration covariance (unknown)
        msg.linear_acceleration_covariance = [0.0] * 9

        # Publish the message
        self.publisher.publish(msg)

        # Increment sequence number
        self.sequence_number += 1

        # Log the published data periodically
        if self.sequence_number % 50 == 0:  # Log every 50 messages (1 Hz)
            self.get_logger().info(
                f'Published IMU data: orientation.z={msg.orientation.z:.3f}, '
                f'linear_acc.x={msg.linear_acceleration.x:.3f}'
            )

    def calibrate_sensor_callback(self, request, response):
        """
        Callback function for the calibration service.

        Args:
            request: The service request (Trigger request)
            response: The service response to be filled

        Returns:
            The response object with success status and message
        """
        try:
            # Perform calibration (in this example, reset the offset)
            self.calibration_offset = 0.0

            # Simulate calibration process
            time.sleep(0.1)  # Simulate time needed for calibration

            # Set response
            response.success = True
            response.message = "Sensor calibrated successfully"

            self.get_logger().info('Sensor calibrated successfully')

        except Exception as e:
            response.success = False
            response.message = f"Calibration failed: {str(e)}"
            self.get_logger().error(f'Calibration error: {str(e)}')

        return response


def main(args=None):
    """
    Main function to initialize and run the sensor node.

    Args:
        args: Command line arguments (default: None)
    """
    # Initialize the ROS 2 client library
    rclpy.init(args=args)

    # Create the sensor node
    sensor_node = SensorNode()

    try:
        # Spin the node to process callbacks
        rclpy.spin(sensor_node)
    except KeyboardInterrupt:
        # Handle graceful shutdown when Ctrl+C is pressed
        pass
    finally:
        # Clean up resources
        sensor_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()