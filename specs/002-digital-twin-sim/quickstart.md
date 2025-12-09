# Quickstart Guide: Module 2 — The Digital Twin (Simulation Environment)

## Prerequisites

- Gazebo Garden (or Citadel) installed
- Unity 2022.3 LTS installed
- ROS 2 Humble installed and sourced
- Basic knowledge of simulation concepts and robotics

## Setup Instructions

### 1. Environment Setup
```bash
# Verify Gazebo installation
gz --version

# Verify ROS 2 installation
source /opt/ros/humble/setup.bash
ros2 topic list

# Verify Unity installation (check Unity Hub or Unity executable)
```

### 2. Project Structure
```
book/
├── docs/
│   └── module2/                # Module 2 content
│       ├── chapter1-physics-foundations/
│       ├── chapter2-gazebo-environment/
│       ├── chapter3-sensor-simulation/
│       └── chapter4-unity-visualization/
├── simulations/
│   ├── gazebo-worlds/          # Gazebo simulation files
│   │   ├── basic-physics-world/
│   │   ├── humanoid-robot-world/
│   │   └── sensor-test-worlds/
│   └── unity-scenes/           # Unity scene files
│       ├── basic-visualization/
│       └── human-robot-interaction/
└── static/                     # Static assets and diagrams
```

## Running Gazebo Simulations

### 1. Basic Physics World
```bash
# Navigate to the physics world directory
cd simulations/gazebo-worlds/basic-physics-world

# Launch the simulation
gz sim -r physics_world.sdf
```

### 2. Humanoid Robot World
```bash
# Navigate to the humanoid world directory
cd simulations/gazebo-worlds/humanoid-robot-world

# Launch the simulation with a humanoid robot
gz sim -r humanoid_world.sdf

# In another terminal, check available topics
gz topic -l
```

### 3. Sensor Testing Worlds
```bash
# Navigate to sensor test worlds
cd simulations/gazebo-worlds/sensor-test-worlds

# Launch LiDAR sensor test world
gz sim -r lidar_test.sdf

# Launch IMU sensor test world
gz sim -r imu_test.sdf

# Launch depth sensor test world
gz sim -r depth_test.sdf
```

## Creating Content

### 1. Add a New Chapter
Create a new MDX file in the appropriate module2 subdirectory:

```bash
# Create a new section in the physics foundations chapter
touch docs/module2/chapter1-physics-foundations/new-section.mdx
```

### 2. Basic MDX Structure with Simulation Content
```mdx
---
title: Physics Simulation Concepts
description: Understanding physics simulation for robotics
sidebar_position: 1
---

# Physics Simulation Concepts

This chapter covers the fundamentals of physics simulation for robotics applications.

## Basic Physics Concepts

In simulation environments, physics properties determine how objects interact with each other and the environment.

### Gravity

Gravity is a fundamental force in physics simulation:

```xml
<world>
  <physics>
    <gravity>0 0 -9.8</gravity>
  </physics>
</world>
```

## Simulation Example

<SimulationExample id="basic-physics-world" title="Basic Physics World" type="gazebo-world">
  This example demonstrates basic physics properties including gravity, friction, and collision detection.
</SimulationExample>
```

### 3. Adding Gazebo Worlds
Create SDF files for Gazebo simulations:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="physics_world">
    <physics type="ode">
      <gravity>0 0 -9.8</gravity>
    </physics>

    <model name="ground_plane">
      <pose>0 0 0 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
            </plane>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>10 10</size>
            </plane>
          </geometry>
        </visual>
      </link>
    </model>
  </world>
</sdf>
```

### 4. Adding Unity Scenes
Unity scenes should be created in the Unity editor and exported to the appropriate directory. Each scene should include:
- 3D models for robots and environment
- Lighting configuration
- Camera setup for visualization
- Scripts for data integration

## Building for Production

### 1. Docusaurus Build
```bash
# Navigate to book directory
cd book/

# Build the static files for deployment
npm run build

# The static files will be generated in the build/ directory
```

### 2. Simulation Validation
```bash
# Validate all Gazebo worlds
cd simulations/gazebo-worlds/
find . -name "*.sdf" -exec gz sdf -k {} \;

# Test each world briefly
gz sim -r basic-physics-world/physics_world.sdf --headless-rendering
```

## Testing

### 1. Content Validation
```bash
# Run Docusaurus validation
npm run serve

# Check for broken links
npx @docusaurus/plugin-client-redirects validate-links
```

### 2. Simulation Testing
```bash
# Test each simulation world
cd simulations/gazebo-worlds/basic-physics-world
gz sim -r physics_world.sdf --iterations 100

cd ../humanoid-robot-world
gz sim -r humanoid_world.sdf --iterations 100

cd ../sensor-test-worlds
gz sim -r lidar_test.sdf --iterations 100
gz sim -r imu_test.sdf --iterations 100
gz sim -r depth_test.sdf --iterations 100
```

## Common Commands

```bash
# List all available Gazebo topics
gz topic -l

# Echo a specific topic (e.g., IMU data)
gz topic -e -t /imu

# List all models in the simulation
gz model -l

# Reset the simulation
gz service -s /world/reset --reqtype ignition.msgs.WorldReset --req 'all: true'
```

## Troubleshooting

### Common Issues

1. **Gazebo fails to start**: Ensure GPU drivers are properly installed and X11 forwarding is enabled if using SSH.

2. **Simulation runs slowly**: Reduce physics complexity or use simpler collision geometries.

3. **Unity scenes not loading**: Verify Unity version compatibility and check that all assets are properly imported.

4. **ROS 2 integration issues**: Ensure ROS 2 humble is sourced in the same terminal as Gazebo launch.

### Performance Tips

- Use simplified collision meshes for better performance
- Limit the number of active sensors in a single simulation
- Use appropriate update rates for sensors (e.g., 30Hz for cameras, 100Hz for IMU)
- Consider using GPU acceleration for rendering-intensive tasks