# Quickstart Guide: AI/Spec-driven Book using Docusaurus

## Prerequisites

- Node.js v18+ installed
- npm or yarn package manager
- Git for version control
- Basic knowledge of React and MDX

## Setup Instructions

### 1. Clone and Initialize
```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Install dependencies
npm install
# OR
yarn install
```

### 2. Local Development
```bash
# Start the development server
npm run start
# OR
yarn start

# This command starts a local development server and opens up a browser window.
# Most changes are reflected live without having to restart the server.
```

### 3. Project Structure
```
book/
├── docs/                 # Content files organized by phase
│   ├── research/         # Research phase content
│   ├── foundation/       # Foundation phase content
│   ├── analysis/         # Analysis phase content
│   └── synthesis/        # Synthesis phase content
├── src/
│   ├── components/       # Custom React components
│   ├── pages/            # Additional pages
│   └── css/              # Custom styles
├── static/               # Static assets
├── docusaurus.config.js  # Main configuration
├── sidebars.js           # Navigation structure
├── package.json          # Dependencies and scripts
└── mdx-components.js     # MDX component mapping
```

## Creating Content

### 1. Add a New Chapter
Create a new MDX file in the appropriate phase directory:

```bash
# Create a new chapter in the research phase
touch docs/research/new-chapter.mdx
```

### 2. Basic MDX Structure
```mdx
---
title: Your Chapter Title
description: Brief description of the chapter
sidebar_position: 1
---

# Your Chapter Title

Content goes here...

## Section Title

More content...

### Subsection Title

Even more content...
```

### 3. Adding APA Citations
Use the custom citation component:

```mdx
For more information on humanoid robotics, see <Citation id="author2023title" />.

<CitationList />
```

### 4. Adding Code Examples
```mdx
import CodeBlock from '@theme/CodeBlock';
import { python } from 'prism-react-renderer';

<CodeBlock language="python">
```python
# Your Python code here
def example_function():
    return "Hello, World!"
```
</CodeBlock>
```

### 5. Adding Diagrams
```mdx
import Mermaid from '@theme/Mermaid';

<Mermaid>
graph TD;
    A[Start] --> B{Decision};
    B -->|Yes| C[Action 1];
    B -->|No| D[Action 2];
</Mermaid>
```

## Building for Production

```bash
# Build the static files for deployment
npm run build
# OR
yarn build

# The static files will be generated in the build/ directory
```

## Testing

### 1. Run Tests
```bash
# Run unit tests
npm run test
# OR
yarn test

# Run linting
npm run lint
# OR
yarn lint

# Run type checking (if using TypeScript)
npm run type-check
# OR
yarn type-check
```

### 2. Validate Citations
```bash
# Check for APA citation compliance
npm run validate-citations
# OR
yarn validate-citations
```

## Deployment

### GitHub Pages
```bash
# Deploy to GitHub Pages
npm run deploy
# OR
yarn deploy
```

### Other Platforms
For deployment to Vercel, Netlify, or other platforms, simply deploy the contents of the `build/` directory.

## Common Commands

```bash
# Clean and reinstall dependencies
npm run clean && npm install

# Serve the built site locally for testing
npm run serve
# OR
yarn serve

# Generate a new phase
npm run create-phase -- research
# OR
yarn create-phase -- research
```

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in docusaurus.config.js or use a different port:
   ```bash
   npm run start -- --port 3001
   ```

2. **Build fails**: Clear cache and reinstall:
   ```bash
   npx docusaurus clear && npm install && npm run build
   ```

3. **Citation formatting issues**: Check that all citations follow APA format and are properly referenced in the bibliography.