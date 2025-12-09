# Quickstart Guide: Module 3 — The AI-Robot Brain (Perception & Navigation System)

## Prerequisites

- NVIDIA Isaac Sim installed (with Omniverse access)
- Isaac ROS packages installed
- ROS 2 Humble installed and sourced
- Nav2 navigation stack installed
- NVIDIA GPU with CUDA support
- Basic knowledge of perception and navigation concepts

## Setup Instructions

### 1. Environment Setup
```bash
# Verify Isaac Sim installation
isaac-sim --version

# Verify ROS 2 installation
source /opt/ros/humble/setup.bash
ros2 topic list

# Verify Isaac ROS packages
ros2 pkg list | grep isaac_ros

# Verify Nav2 installation
ros2 pkg list | grep nav2
```

### 2. Project Structure
```
book/
├── docs/
│   └── module3/                    # Module 3 content
│       ├── chapter1-perception-fundamentals/
│       ├── chapter2-vslam-systems/
│       ├── chapter3-navigation-planning/
│       └── chapter4-perception-navigation-integration/
├── perception/
│   ├── synthetic-data/             # Synthetic dataset generation
│   │   ├── dataset-generation/
│   │   └── domain-randomization/
│   ├── vslam-pipeline/             # VSLAM implementation
│   │   ├── feature-detection/
│   │   ├── pose-estimation/
│   │   └── mapping/
│   └── sensors/                    # Sensor simulation
│       ├── camera-sim/
│       └── lidar-sim/
├── navigation/
│   ├── nav2-config/                # Nav2 configuration files
│   ├── path-planning/              # Path planning algorithms
│   └── biped-control/              # Biped locomotion controllers
└── static/                         # Static assets and diagrams
```

## Running Perception Examples

### 1. Synthetic Data Generation
```bash
# Navigate to synthetic data directory
cd perception/synthetic-data/dataset-generation

# Run the dataset generation script
python3 generate_dataset.py --output-path ./datasets/synthetic_data
```

### 2. VSLAM Pipeline
```bash
# Navigate to VSLAM pipeline directory
cd perception/vslam-pipeline

# Launch the VSLAM pipeline with Isaac ROS
ros2 launch isaac_ros_vslam isaac_ros_vslam.launch.py
```

### 3. Feature Detection
```bash
# Navigate to feature detection directory
cd perception/vslam-pipeline/feature-detection

# Run feature detection example
python3 feature_detection.py --input-source camera_topic
```

## Running Navigation Examples

### 1. Nav2 Configuration
```bash
# Navigate to Nav2 configuration directory
cd navigation/nav2-config

# Launch Nav2 with custom biped configuration
ros2 launch nav2_bringup navigation_launch.py \
  params_file:=./config/biped_nav2_params.yaml
```

### 2. Path Planning
```bash
# Navigate to path planning directory
cd navigation/path-planning

# Run path planning example
python3 path_planner.py --start-x 0 --start-y 0 --goal-x 10 --goal-y 10
```

### 3. Biped Control
```bash
# Navigate to biped control directory
cd navigation/biped-control

# Launch biped controller
ros2 launch biped_controller biped_control.launch.py
```

## Creating Content

### 1. Add a New Chapter
Create a new MDX file in the appropriate module3 subdirectory:

```bash
# Create a new section in the perception fundamentals chapter
touch docs/module3/chapter1-perception-fundamentals/new-section.mdx
```

### 2. Basic MDX Structure with Perception/Navigation Content
```mdx
---
title: Perception Fundamentals
description: Understanding perception systems for robotics
sidebar_position: 1
---

# Perception Fundamentals

This chapter covers the fundamentals of perception systems for robotics applications.

## Synthetic Data Generation

Synthetic data is crucial for training perception systems:

```python
import omni.synthetic_utils as synth

# Generate synthetic dataset with domain randomization
dataset = synth.generate_dataset(
    objects=["robot", "obstacles"],
    lighting_conditions=["indoor", "outdoor"],
    textures=["metal", "wood", "plastic"]
)
```

## Perception Example

<PerceptionExample id="vslam-pipeline" title="VSLAM Pipeline" type="vslam-pipeline">
  This example demonstrates a complete Visual SLAM pipeline using Isaac ROS.
</PerceptionExample>
```

### 3. Adding Isaac Sim Worlds
Isaac Sim worlds should be created using the Isaac Sim application and saved to the appropriate directory. Each world should include:
- 3D models for robots and environment
- Sensor configurations
- Lighting setup
- Domain randomization parameters

### 4. Adding ROS 2 Launch Files
Create launch files for Isaac ROS and Nav2 integration:

```xml
<launch>
  <!-- Isaac ROS VSLAM components -->
  <node pkg="isaac_ros_visual_slam" exec="visual_slam_node" name="visual_slam_node">
    <param name="enable_rectified_edge" value="true"/>
    <param name="enable_debug_mode" value="false"/>
  </node>

  <!-- Nav2 navigation stack -->
  <include file="$(find-pkg-share nav2_bringup)/launch/navigation_launch.py">
    <arg name="params_file" value="$(find-pkg-share my_robot)/config/nav2_params.yaml"/>
  </include>
</launch>
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

### 2. Perception/Navigation Validation
```bash
# Validate Isaac Sim worlds
cd perception/synthetic-data/
# Check that all required assets exist and are accessible

# Test VSLAM pipeline
cd perception/vslam-pipeline/
python3 test_pipeline.py

# Test Nav2 configuration
cd navigation/nav2-config/
ros2 launch nav2_bringup navigation_launch.py --dry-run
```

## Testing

### 1. Content Validation
```bash
# Run Docusaurus validation
npm run serve

# Check for broken links
npx @docusaurus/plugin-client-redirects validate-links
```

### 2. Perception System Testing
```bash
# Test synthetic data generation
cd perception/synthetic-data/dataset-generation
python3 generate_dataset.py --test-mode

# Test VSLAM pipeline
cd perception/vslam-pipeline
ros2 launch isaac_ros_vslam test_vslam.launch.py
```

### 3. Navigation System Testing
```bash
# Test Nav2 configuration
cd navigation/nav2-config
ros2 launch nav2_bringup test_navigation.launch.py

# Test path planning
cd navigation/path-planning
python3 test_path_planner.py
```

## Common Commands

```bash
# List all Isaac ROS nodes
ros2 node list | grep isaac

# Echo VSLAM pose estimates
ros2 topic echo /visual_slam/pose_graph/poses

# List Nav2-related topics
ros2 topic list | grep nav

# Check Nav2 server status
ros2 action list | grep navigate
```

## Troubleshooting

### Common Issues

1. **CUDA/Isaac Sim issues**: Ensure NVIDIA GPU drivers are properly installed and CUDA is accessible.

2. **Isaac Sim licensing**: Verify Isaac Sim and Omniverse credentials are properly configured.

3. **ROS 2 integration problems**: Ensure all packages are properly sourced and dependencies are installed.

4. **Performance issues**: Perception algorithms can be computationally intensive; ensure adequate GPU resources.

### Performance Tips

- Use optimized Isaac ROS packages for better performance
- Consider running synthetic data generation in batches
- Use appropriate image resolutions for VSLAM (e.g., 640x480 instead of 4K)
- Profile navigation algorithms to identify bottlenecks
- Use Nav2's lifecycle nodes for better resource management