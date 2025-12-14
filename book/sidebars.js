// @type import('@docusaurus/module-type-aliases').Config

/** @type {import('@docusaurus/types').Config} */
const config = {
  tutorial: [
    'intro',
    {
      type: 'category',
      label: 'Research Phase',
      items: [
        'research/chapter-1-speech-processing',
        'research/speech-pipeline',
        'research/bibliography'
      ],
    },
    {
      type: 'category',
      label: 'Foundation Phase',
      items: [
        'foundation/chapter-1-language-models',
        'foundation/prompt-templates',
        'foundation/bibliography'
      ],
    },
    {
      type: 'category',
      label: 'Analysis Phase',
      items: [
        'analysis/chapter-1-action-mapping',
        'analysis/robot-communication-protocols',
        'analysis/bibliography'
      ],
    },
    {
      type: 'category',
      label: 'Synthesis Phase',
      items: [
        'synthesis/chapter-1-vla-integration',
        'synthesis/vla-pipeline',
        'synthesis/bibliography'
      ],
    },
    {
      type: 'category',
      label: 'Cross-References',
      items: [
        'bibliography'
      ],
    },
    'module1/intro',
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System',
      items: [
        'module1/chapter1-robot-communication-fundamentals/communication-fundamentals',
        'module1/chapter1-robot-communication-fundamentals/nodes-concept',
        'module1/chapter1-robot-communication-fundamentals/topics-concept',
        'module1/chapter1-robot-communication-fundamentals/services-concept',
        'module1/chapter2-node-implementation-and-control/node-implementation',
        'module1/chapter2-node-implementation-and-control/lifecycle',
        'module1/chapter2-node-implementation-and-control/qos',
        'module1/chapter3-robot-structure-description/robot-description',
        'module1/chapter3-robot-structure-description/urdf-explanation',
        'module1/chapter3-robot-structure-description/xacro-explanation',
        'module1/chapter3-robot-structure-description/links-joints',
        'module1/chapter4-advanced-communication-patterns/advanced-patterns',
        'module1/chapter4-advanced-communication-patterns/actions',
        'module1/chapter4-advanced-communication-patterns/lifecycle-nodes',
        'module1/troubleshooting'
      ],
    },
    'module2/intro',
    {
      type: 'category',
      label: 'Module 2: The Virtual Robotics Laboratory (Gazebo & Simulation)',
      items: [
        'module2/chapter1-simulation-fundamentals/simulation-fundamentals',
        'module2/chapter1-simulation-fundamentals/physics-concept',
        'module2/chapter1-simulation-fundamentals/sensors-concept',
        'module2/chapter1-simulation-fundamentals/environment-concept',
        'module2/chapter2-gazebo-environment/gazebo-environment',
        {
          type: 'category',
          label: 'Environment Setup and Configuration',
          items: [
            'module2/chapter2-gazebo-environment/sub-chapters/environment-setup',
            'module2/chapter2-gazebo-environment/sub-chapters/world-building',
            'module2/chapter2-gazebo-environment/sub-chapters/model-integration'
          ]
        },
        'module2/chapter3-robot-modeling/robot-modeling',
        {
          type: 'category',
          label: 'Modeling Fundamentals',
          items: [
            'module2/chapter3-robot-modeling/sub-chapters/urdf-fundamentals',
            'module2/chapter3-robot-modeling/sub-chapters/sensors-controllers',
            'module2/chapter3-robot-modeling/sub-chapters/model-validation'
          ]
        },
        'module2/chapter4-advanced-techniques/advanced-techniques',
        {
          type: 'category',
          label: 'Advanced Techniques',
          items: [
            'module2/chapter4-advanced-techniques/sub-chapters/multi-robot-coordination',
            'module2/chapter4-advanced-techniques/sub-chapters/physics-tuning',
            'module2/chapter4-advanced-techniques/sub-chapters/performance-optimization'
          ]
        }
      ],
    }
  ],
};

module.exports = config;