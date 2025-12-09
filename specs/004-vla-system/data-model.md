# Data Model: AI/Spec-driven Book using Docusaurus

## Content Entities

### Book
- **Fields**:
  - id: string (unique identifier)
  - title: string (title of the book)
  - description: string (brief description)
  - author: string (author name)
  - version: string (version number)
  - phases: Phase[] (list of phases in the book)
  - createdAt: Date (creation timestamp)
  - updatedAt: Date (last update timestamp)

- **Relationships**:
  - Contains many Phases
  - Associated with many Citations

### Phase
- **Fields**:
  - id: string (unique identifier)
  - title: string (title of the phase)
  - description: string (brief description)
  - order: number (sequence order in the book)
  - chapters: Chapter[] (list of chapters in the phase)
  - status: enum (draft, review, published)

- **Relationships**:
  - Belongs to one Book
  - Contains many Chapters
  - Contains many Sections

### Chapter
- **Fields**:
  - id: string (unique identifier)
  - title: string (title of the chapter)
  - description: string (brief description)
  - content: string (main content in MDX format)
  - wordCount: number (approximate word count)
  - order: number (sequence order in the phase)
  - status: enum (draft, review, published)
  - createdAt: Date (creation timestamp)
  - updatedAt: Date (last update timestamp)

- **Relationships**:
  - Belongs to one Phase
  - Contains many Sections
  - Associated with many Citations

### Section
- **Fields**:
  - id: string (unique identifier)
  - title: string (title of the section)
  - content: string (section content in MDX format)
  - order: number (sequence order in the chapter)
  - sectionType: enum (text, code, diagram, exercise)

- **Relationships**:
  - Belongs to one Chapter
  - Associated with many Citations

### Citation
- **Fields**:
  - id: string (unique identifier)
  - type: enum (book, article, website, paper, etc.)
  - author: string (author name)
  - title: string (title of the work)
  - publisher: string (publisher name)
  - year: number (publication year)
  - url: string (optional URL)
  - apaFormatted: string (APA formatted citation)
  - contentReference: string (reference to where it's cited)

- **Relationships**:
  - Associated with one or more Chapters
  - Associated with one or more Sections

### CodeExample
- **Fields**:
  - id: string (unique identifier)
  - title: string (title of the example)
  - description: string (brief description)
  - code: string (the actual code)
  - language: string (programming language)
  - runnable: boolean (whether the example can be run)
  - phase: enum (which phase it belongs to)

- **Relationships**:
  - Associated with one or more Chapters
  - Associated with one or more Sections

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

### Book
- Title must be 1-200 characters
- Description must be 1-500 characters
- Must have at least one phase
- Version must follow semantic versioning

### Phase
- Title must be 1-100 characters
- Order must be a positive integer
- Must have a valid status value
- Must belong to exactly one book

### Chapter
- Title must be 1-100 characters
- Content must be valid MDX
- Word count must be positive
- Order must be a positive integer
- Status must be valid

### Section
- Title must be 1-100 characters
- Order must be a positive integer
- Section type must be valid

### Citation
- Author and title are required
- Year must be a valid year (1000-2100)
- APA format must be valid according to constitution requirements

## State Transitions

### Chapter Status
- draft → review: When initial content is completed
- review → published: When content passes quality validation
- published → review: When content needs updates
- review → draft: When major changes are needed

### Phase Status
- draft → review: When all chapters in the phase are in review status
- review → published: When all chapters in the phase are published
- published → review: When any chapter in the phase changes to review