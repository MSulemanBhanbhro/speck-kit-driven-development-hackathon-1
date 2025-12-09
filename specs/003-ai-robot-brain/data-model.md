# Data Model: Module 3 — The AI-Robot Brain (Perception & Navigation System)

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
  - Associated with many PerceptionExamples
  - Associated with many NavigationExamples
  - Associated with many Diagrams

### Section
- **Fields**:
  - id: string (unique identifier)
  - title: string (title of the section)
  - content: string (section content in MDX format)
  - order: number (sequence order in the chapter)
  - sectionType: enum (text, code, diagram, exercise, perception, navigation)

- **Relationships**:
  - Belongs to one Chapter
  - Associated with one or more PerceptionExamples or NavigationExamples

### PerceptionExample
- **Fields**:
  - id: string (unique identifier)
  - title: string (title of the example)
  - description: string (brief description)
  - type: enum (synthetic-data, vslam-pipeline, feature-detection, pose-estimation, mapping)
  - scriptPath: string (path to the Python/script file)
  - runnable: boolean (whether the example can be executed)
  - requirements: string[] (dependencies needed to run the example)
  - datasetPath: string (path to associated dataset if applicable)

- **Relationships**:
  - Associated with one or more Chapters
  - Associated with one or more Sections

### NavigationExample
- **Fields**:
  - id: string (unique identifier)
  - title: string (title of the example)
  - description: string (brief description)
  - type: enum (nav2-config, path-planning, biped-control, localization)
  - scriptPath: string (path to the ROS 2/Nav2 script)
  - runnable: boolean (whether the example can be executed)
  - requirements: string[] (dependencies needed to run the example)
  - worldPath: string (path to associated Gazebo/Isaac Sim world)

- **Relationships**:
  - Associated with one or more Chapters
  - Associated with one or more Sections

### Dataset
- **Fields**:
  - id: string (unique identifier)
  - name: string (name of the dataset)
  - description: string (brief description)
  - size: number (size in MB/GB)
  - format: enum (image, pointcloud, lidar, camera, imu)
  - source: enum (synthetic, real-world, mixed)
  - syntheticMethod: string (how synthetic data was generated)
  - path: string (path to dataset files)

- **Relationships**:
  - Associated with one or more PerceptionExamples
  - Associated with one or more PerceptionPipelines

### PerceptionPipeline
- **Fields**:
  - id: string (unique identifier)
  - name: string (name of the pipeline)
  - description: string (brief description)
  - type: enum (vslam, vio, feature-detection, object-detection)
  - components: string[] (list of pipeline components)
  - inputType: string (type of input data)
  - outputType: string (type of output data)
  - performanceMetrics: object (fps, accuracy, etc.)

- **Relationships**:
  - Associated with one or more PerceptionExamples
  - Associated with one or more NavigationExamples (for integrated systems)

### NavigationSystem
- **Fields**:
  - id: string (unique identifier)
  - name: string (name of the navigation system)
  - description: string (brief description)
  - locomotionType: enum (biped, wheeled, tracked, flying)
  - planners: string[] (global and local planners used)
  - controllers: string[] (motion controllers)
  - sensors: string[] (sensors used for navigation)
  - performanceMetrics: object (planning time, success rate, etc.)

- **Relationships**:
  - Associated with one or more NavigationExamples
  - Associated with one or more PerceptionPipelines (for integrated systems)

### IsaacSimWorld
- **Fields**:
  - id: string (unique identifier)
  - name: string (name of the Isaac Sim world)
  - description: string (brief description)
  - path: string (path to the Isaac Sim world file)
  - sensors: string[] (sensors configured in the world)
  - lighting: object (lighting configuration)
  - objects: object[] (list of objects in the world)

- **Relationships**:
  - Associated with one or more PerceptionExamples
  - Associated with one or more NavigationExamples

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

### PerceptionExample
- Title and description are required
- Type must be valid
- Script path must exist and be accessible
- Requirements must be properly formatted

### NavigationExample
- Title and description are required
- Type must be valid
- Script path must exist and be accessible
- Requirements must be properly formatted

### Dataset
- Name and description are required
- Size must be positive
- Format and source must be valid
- Path must point to a valid dataset

### PerceptionPipeline
- Name and description are required
- Type must be valid
- Components must be properly specified
- Performance metrics must have valid ranges

### NavigationSystem
- Name and description are required
- Locomotion type must be valid
- Planners and controllers must be properly specified

## State Transitions

### Chapter Status
- draft → review: When initial content is completed
- review → published: When content passes quality validation
- published → review: When content needs updates
- review → draft: When major changes are needed