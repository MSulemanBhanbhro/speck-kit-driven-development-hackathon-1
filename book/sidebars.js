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
    }
  ],
};

module.exports = config;