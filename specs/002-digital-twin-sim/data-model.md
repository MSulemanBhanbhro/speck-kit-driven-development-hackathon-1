# Data Model: Module 2 — The Digital Twin (Simulation Environment)

## Content Entities

### Chapter
- **Fields**:
  - id: string (unique identifier)
  - title: string (title of the chapter)
  - description: string (brief description)
  - content: string (main content in MDX format)
  - wordCount: number (approximate word count)
  - order: number (sequence order in the module: 1-4)
  - status: enum (draft, review, published)
  - createdAt: Date (creation timestamp)
  - updatedAt: Date (last update timestamp)

- **Relationships**:
  - Belongs to one Module
  - Contains many Sections
  - Associated with many SimulationExamples
  - Associated with many Diagrams

### Section
- **Fields**:
  - id: string (unique identifier)
  - title: string (title of the section)
  - content: string (section content in MDX format)
  - order: number (sequence order in the chapter)
  - sectionType: enum (text, code, diagram, exercise, simulation)

- **Relationships**:
  - Belongs to one Chapter
  - Associated with one or more SimulationExamples

### SimulationExample
- **Fields**:
  - id: string (unique identifier)
  - title: string (title of the example)
  - description: string (brief description)
  - type: enum (gazebo-world, unity-scene, robot-model, sensor-config, spawn-script)
  - filePath: string (path to the simulation file)
  - runnable: boolean (whether the example can be executed)
  - requirements: string[] (dependencies needed to run the example)

- **Relationships**:
  - Associated with one or more Chapters
  - Associated with one or more Sections

### GazeboWorld
- **Fields**:
  - id: string (unique identifier)
  - name: string (name of the world)
  - description: string (brief description)
  - sdfContent: string (SDF XML content)
  - physicsProperties: object (gravity, friction, etc.)
  - models: GazeboModel[] (models included in the world)
  - lighting: object (lighting configuration)

- **Relationships**:
  - Associated with one or more SimulationExamples
  - Associated with many GazeboModels

### GazeboModel
- **Fields**:
  - id: string (unique identifier)
  - name: string (name of the model)
  - sdfContent: string (SDF XML content)
  - visualProperties: object (color, material, etc.)
  - collisionProperties: object (collision shapes)
  - jointProperties: object (joint types and constraints)
  - sensors: GazeboSensor[] (sensors attached to the model)

- **Relationships**:
  - Belongs to one or more GazeboWorlds
  - Contains many GazeboSensors

### GazeboSensor
- **Fields**:
  - id: string (unique identifier)
  - type: enum (lidar, imu, depth, camera, gps, imu)
  - name: string (name of the sensor)
  - configuration: object (sensor-specific parameters)
  - topic: string (ROS topic for sensor data)
  - updateRate: number (frequency of sensor updates)

- **Relationships**:
  - Belongs to one GazeboModel
  - Associated with one or more SimulationExamples

### UnityScene
- **Fields**:
  - id: string (unique identifier)
  - name: string (name of the scene)
  - description: string (brief description)
  - filePath: string (path to the .unity file)
  - objects: UnityObject[] (game objects in the scene)
  - lighting: object (lighting configuration)
  - cameraSettings: object (camera configuration)

- **Relationships**:
  - Associated with one or more SimulationExamples
  - Contains many UnityObjects

### UnityObject
- **Fields**:
  - id: string (unique identifier)
  - name: string (name of the object)
  - type: enum (robot, sensor, environment, ui-element)
  - position: object (x, y, z coordinates)
  - rotation: object (x, y, z, w quaternion)
  - scale: object (x, y, z scale factors)
  - components: string[] (attached Unity components)

- **Relationships**:
  - Belongs to one UnityScene
  - Associated with one or more SimulationExamples

### Diagram
- **Fields**:
  - id: string (unique identifier)
  - title: string (title of the diagram)
  - description: string (brief description)
  - type: enum (mermaid, svg, image)
  - content: string (diagram definition or path)
  - altText: string (accessibility text)

- **Relationships**:
  - Associated with one or more Chapters
  - Associated with one or more Sections

## Validation Rules

### Chapter
- Title must be 1-100 characters
- Content must be valid MDX
- Word count must be between 750-1250
- Order must be between 1-4 for this module
- Status must be valid

### Section
- Title must be 1-100 characters
- Order must be a positive integer
- Section type must be valid

### SimulationExample
- Title and description are required
- Type must be valid
- File path must exist and be accessible
- Requirements must be properly formatted

### GazeboWorld
- Name must be unique within the module
- SDF content must be valid XML
- Physics properties must have valid values

### GazeboModel
- Name must be unique within the world
- SDF content must be valid XML
- Joint properties must be physically valid

### GazeboSensor
- Type must be valid
- Update rate must be positive
- Topic must follow ROS naming conventions

### UnityScene
- Name must be unique within the module
- File path must point to a valid Unity scene
- Objects must have valid transforms

## State Transitions

### Chapter Status
- draft → review: When initial content is completed
- review → published: When content passes quality validation
- published → review: When content needs updates
- review → draft: When major changes are needed