# Quickstart Guide: Module 1 — The Robotic Nervous System (Robot Operating System)

## Prerequisites

- Ubuntu 22.04 LTS
- ROS 2 Humble Hawksbill installed and sourced
- Python 3.8+ development environment
- Basic knowledge of Python programming
- Understanding of basic robotics concepts

## Setup Instructions

### 1. Environment Setup
```bash
# Verify ROS 2 installation
source /opt/ros/humble/setup.bash
ros2 --version

# Create a workspace for examples
mkdir -p ~/ros2_examples_ws/src
cd ~/ros2_examples_ws

# Source the workspace
source install/setup.bash
```

### 2. Project Structure
```
book/
├── docs/
│   └── module1/                    # Module 1 content
│       ├── chapter1-robot-communication-fundamentals/
│       ├── chapter2-node-implementation-and-control/
│       ├── chapter3-robot-structure-description/
│       └── chapter4-advanced-communication-patterns/
├── ros_examples/                   # ROS 2 example code
│   ├── basic_publisher/
│   ├── basic_subscriber/
│   ├── service_server/
│   ├── service_client/
│   ├── action_server/
│   ├── action_client/
│   └── robot_description/
│       ├── urdf/
│       └── launch/
└── static/                         # Static assets and diagrams
```

## Running Basic Communication Examples

### 1. Publisher Example
```bash
# Navigate to publisher directory
cd ros_examples/basic_publisher

# Build the package
cd ~/ros2_examples_ws
colcon build --packages-select basic_publisher

# Source the workspace
source install/setup.bash

# Run the publisher
ros2 run basic_publisher talker
```

### 2. Subscriber Example
```bash
# In a new terminal, navigate and source the workspace
cd ~/ros2_examples_ws
source install/setup.bash

# Run the subscriber
ros2 run basic_subscriber listener
```

### 3. Service Example
```bash
# Terminal 1: Run the service server
cd ~/ros2_examples_ws
source install/setup.bash
ros2 run service_server server

# Terminal 2: Call the service
cd ~/ros2_examples_ws
source install/setup.bash
ros2 run service_client client
```

### 4. Action Example
```bash
# Terminal 1: Run the action server
cd ~/ros2_examples_ws
source install/setup.bash
ros2 run action_server server

# Terminal 2: Run the action client
cd ~/ros2_examples_ws
source install/setup.bash
ros2 run action_client client
```

## Creating Robot Descriptions

### 1. Basic URDF Robot
```bash
# Navigate to robot description directory
cd ros_examples/robot_description/urdf

# Create a simple humanoid robot description
touch simple_humanoid.urdf

# Visualize the robot in RViz
ros2 launch robot_state_publisher robot_state_publisher.launch.py \
  urdf_file:=simple_humanoid.urdf
```

### 2. XACRO Robot Description
```bash
# Create a more complex robot using XACRO
touch complex_humanoid.xacro

# Process XACRO to URDF
ros2 run xacro xacro complex_humanoid.xacro > processed_robot.urdf
```

## Creating Content

### 1. Add a New Chapter
Create a new MDX file in the appropriate module1 subdirectory:

```bash
# Create a new section in the communication fundamentals chapter
touch docs/module1/chapter1-robot-communication-fundamentals/new-section.mdx
```

### 2. Basic MDX Structure with ROS 2 Content
```mdx
---
title: Robot Communication Fundamentals
description: Understanding ROS 2 communication patterns
sidebar_position: 1
---

# Robot Communication Fundamentals

This chapter covers the fundamentals of ROS 2 communication patterns for robotics applications.

## Publisher-Subscriber Pattern

The publisher-subscriber pattern is fundamental to ROS 2 communication:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1
```

## ROS 2 Example

<ROSExample id="basic-publisher" title="Basic Publisher" type="publisher">
  This example demonstrates a simple publisher that sends messages to a topic.
</ROSExample>
```

### 3. Adding Launch Files
Create launch files for ROS 2 examples:

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='basic_publisher',
            executable='talker',
            name='minimal_publisher',
        ),
        Node(
            package='basic_subscriber',
            executable='listener',
            name='minimal_subscriber',
        ),
    ])
```

## Building for Production

### 1. Docusaurus Build
```bash
# Navigate to book directory
cd book/

# Build the static files for deployment
npm run build

# The static files will be generated in the build/ directory
```

### 2. ROS 2 Package Validation
```bash
# Validate ROS 2 packages
cd ~/ros2_examples_ws
colcon build
source install/setup.bash

# Test basic publisher/subscriber
ros2 run basic_publisher talker &
ros2 run basic_subscriber listener

# Test services
ros2 run service_server server &
ros2 run service_client client

# Test actions
ros2 run action_server server &
ros2 run action_client client
```

## Testing

### 1. Content Validation
```bash
# Run Docusaurus validation
npm run serve

# Check for broken links
npx @docusaurus/plugin-client-redirects validate-links
```

### 2. ROS 2 Testing
```bash
# Build and run tests
cd ~/ros2_examples_ws
colcon build --packages-select basic_publisher basic_subscriber
source install/setup.bash

# Run unit tests
colcon test --packages-select basic_publisher
colcon test-result --all
```

## Common Commands

```bash
# List all ROS 2 nodes
ros2 node list

# Echo a topic
ros2 topic echo /topic std_msgs/msg/String

# List all topics
ros2 topic list

# Call a service
ros2 service call /service_name service_type

# Send an action goal
ros2 action send_goal /action_name action_type "{goal: value}"
```

## Troubleshooting

### Common Issues

1. **Environment not sourced**: Ensure ROS 2 environment is sourced with `source /opt/ros/humble/setup.bash`

2. **Package not found**: Check that packages are built with `colcon build` and workspace is sourced

3. **Permission issues**: Ensure proper permissions on workspace directories

4. **Python path issues**: Verify Python 3.8+ is available and ROS 2 Python packages are installed

### Performance Tips

- Use appropriate QoS settings for your application needs
- Consider message size and frequency for performance
- Use launch files to manage complex node configurations
- Profile node performance to identify bottlenecks
- Use lifecycle nodes for better resource management