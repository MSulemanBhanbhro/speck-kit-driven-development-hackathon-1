<!--
Sync Impact Report:
- Version change: N/A → 1.0.0
- Added principles: Accuracy, Consistency, Educational Clarity, Modularity, Practicality, No Hallucination
- Added sections: Technical Standards, Development Workflow
- Templates requiring updates: ✅ plan-template.md, ✅ spec-template.md, ✅ tasks-template.md
- Follow-up TODOs: RATIFICATION_DATE needs to be set
-->
# AI-Native Book + Integrated RAG Chatbot for Physical AI & Humanoid Robotics Constitution

## Core Principles

### Accuracy
Every technical explanation must be validated against ROS 2, Gazebo, NVIDIA Isaac, and VLA official documentation or academic sources.

### Consistency
Book style, tone, and terminology must remain unified across all chapters generated through Spec-Kit Plus and Claude Code.

### Educational Clarity
Written for students with basic Python + AI knowledge, aiming to understand humanoid robotics from fundamentals to advanced.

### Modularity
Each chapter must work independently while contributing to a coherent unified book structure.

### Practicality
All examples must be runnable using ROS 2, Gazebo, Unity, NVIDIA Isaac Sim, and OpenAI RAG workflow code.

### No Hallucination
Must avoid hallucination; unknown details must be marked clearly.

## Technical Standards
Book format must follow Docusaurus structure with MDX files; All diagrams generated must be reproducible using Mermaid or Code blocks; All code samples must be tested or logically consistent (Python, ROS 2, rclpy, Gazebo plugins, Isaac Sim scripts); Technical claims must reference authoritative sources (ROS docs, NVIDIA docs, robotics research); Writing style: Simple, clean, and structured for learners—grade 9–12 readability; Book must be fully deployable to GitHub Pages using Spec-Kit Plus; RAG chatbot must ONLY answer from book content unless user selects specific text; RAG chatbot integration using FastAPI backend, Neon Serverless Postgres, Qdrant Cloud Free Tier, OpenAI Agents/ChatKit SDKs; RAG pipeline follows text chunking, embedding generation, query → retrieval → LLM answer pattern; The chatbot must embed inside the Docusaurus site as an interactive widget.

## Development Workflow
Minimum 10 full modules/chapters; Every chapter must include: explanation + code + diagrams + exercises; Book length: approx. 30,000–50,000 words; All outputs must be Docusaurus-ready MDX; RAG chatbot code must be production-ready templates and fully integrated; A complete, deployable Docusaurus book is generated; GitHub Pages deployment succeeds without errors; RAG chatbot works end-to-end using OpenAI + FastAPI + Qdrant + Neon; All technical content is valid, verifiable, and consistent; Book demonstrates mastery of Physical AI, Robotics, and RAG systems; Book and chatbot pass manual review with no hallucinations or missing steps.

## Governance
All technical explanations must be validated against authoritative sources; Book style and terminology must remain consistent across all chapters; All examples must be runnable and tested; Docusaurus deployment must succeed without errors; RAG chatbot must work end-to-end using specified technologies; All content must avoid hallucination and mark unknown details clearly; Compliance with ROS 2, Gazebo, NVIDIA Isaac, and VLA official documentation required.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): Original adoption date unknown | **Last Amended**: 2025-12-09
