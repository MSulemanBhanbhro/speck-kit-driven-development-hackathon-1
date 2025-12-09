# Data Model: Module 1 — The Robotic Nervous System (Robot Operating System)

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
  - Associated with many ROSExamples
  - Associated with many RobotDescriptions
  - Associated with many Diagrams

### Section
- **Fields**:
  - id: string (unique identifier)
  - title: string (title of the section)
  - content: string (section content in MDX format)
  - order: number (sequence order in the chapter)
  - sectionType: enum (text, code, diagram, exercise, communication, node, service, action)

- **Relationships**:
  - Belongs to one Chapter
  - Associated with one or more ROSExamples

### ROSExample
- **Fields**:
  - id: string (unique identifier)
  - title: string (title of the example)
  - description: string (brief description)
  - type: enum (publisher, subscriber, service-server, service-client, action-server, action-client, node-implementation)
  - scriptPath: string (path to the Python/C++ script file)
  - runnable: boolean (whether the example can be executed)
  - requirements: string[] (dependencies needed to run the example)
  - launchFile: string (path to associated launch file if applicable)

- **Relationships**:
  - Associated with one or more Chapters
  - Associated with one or more Sections

### RobotDescription
- **Fields**:
  - id: string (unique identifier)
  - name: string (name of the robot description)
  - description: string (brief description)
  - format: enum (urdf, xacro)
  - path: string (path to the robot description file)
  - links: object[] (list of robot links)
  - joints: object[] (list of robot joints)
  - materials: object[] (list of materials used)

- **Relationships**:
  - Associated with one or more Chapters
  - Associated with one or more Sections

### ROSNode
- **Fields**:
  - id: string (unique identifier)
  - name: string (name of the ROS node)
  - description: string (brief description)
  - language: enum (python, cpp)
  - publishers: string[] (list of topics published)
  - subscribers: string[] (list of topics subscribed)
  - services: string[] (list of services provided)
  - actions: string[] (list of actions provided)

- **Relationships**:
  - Associated with one or more ROSExamples
  - Associated with one or more Sections

### Topic
- **Fields**:
  - id: string (unique identifier)
  - name: string (name of the topic)
  - messageType: string (type of message published/subscribed)
  - description: string (brief description)
  - qosProfile: object (Quality of Service profile settings)

- **Relationships**:
  - Associated with ROSNodes (as publishers/subscribers)

### Service
- **Fields**:
  - id: string (unique identifier)
  - name: string (name of the service)
  - serviceType: string (type of service request/response)
  - description: string (brief description)

- **Relationships**:
  - Associated with ROSNodes (as servers/clients)

### Action
- **Fields**:
  - id: string (unique identifier)
  - name: string (name of the action)
  - actionType: string (type of action goal/feedback/result)
  - description: string (brief description)

- **Relationships**:
  - Associated with ROSNodes (as servers/clients)

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
- Word count must be between 750-1300 for individual chapters
- Order must be between 1-4 for this module
- Status must be valid

### Section
- Title must be 1-100 characters
- Order must be a positive integer
- Section type must be valid

### ROSExample
- Title and description are required
- Type must be valid
- Script path must exist and be accessible
- Requirements must be properly formatted

### RobotDescription
- Name and description are required
- Format must be valid
- Path must point to a valid URDF/XACRO file
- Links and joints must be properly structured

### ROSNode
- Name and description are required
- Language must be valid
- Publishers, subscribers, services, and actions must be properly specified

### Topic
- Name and message type are required
- Name must follow ROS naming conventions

### Service
- Name and service type are required
- Name must follow ROS naming conventions

### Action
- Name and action type are required
- Name must follow ROS naming conventions

## State Transitions

### Chapter Status
- draft → review: When initial content is completed
- review → published: When content passes quality validation
- published → review: When content needs updates
- review → draft: When major changes are needed