# Design Agent Workflows

This directory contains n8n workflows for the Design Agent, responsible for generating architecture, PoC documents, and tech stack recommendations.

## Structure

- **`architecture/`** - Workflows for generating High-Level Architecture
- **`poc/`** - Workflows for generating Proof of Concept documents
- **`tech_stack/`** - Workflows for generating Tech Stack Matrix

## Design Agent Functions

### 1. High-Level Architecture Generator
- Takes parsed BRD or engineering plan as input
- Generates system architecture diagrams and descriptions
- Defines components, services, and their interactions
- Output: High-level architecture document

### 2. Proof of Concept (PoC) Generator
- Creates PoC documentation for key features
- Defines validation criteria and approach
- Outlines technical feasibility
- Output: PoC document

### 3. Tech Stack Matrix Generator
- Recommends technology choices
- Compares alternatives with pros/cons
- Aligns with project requirements
- Output: Tech stack recommendation matrix

## Workflow Files

Place exported n8n workflows here with descriptive names:
- `architecture/high_level_architecture_generator.json`
- `poc/poc_document_generator.json`
- `tech_stack/tech_stack_matrix_generator.json`

## Integration Points

- **Input**: Parsed BRD from BRD Parser or plans from Planning Agent
- **Output**: Technical design documents → final deliverables
- **Shared Resources**: Uses shared_nodes for state management and error handling

