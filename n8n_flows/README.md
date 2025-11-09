# n8n Flows

This directory contains exported n8n workflow files in JSON format, organized by agent function.

## Structure

### Agent Workflows

- **`planning_agent/`** - Planning Agent workflows
  - `engineering_plan/` - Workflows for generating Structured Engineering Plans
  - `project_schedule/` - Workflows for generating Project Schedules

- **`design_agent/`** - Design Agent workflows
  - `architecture/` - Workflows for generating High-Level Architecture
  - `poc/` - Workflows for generating Proof of Concept documents
  - `tech_stack/` - Workflows for generating Tech Stack Matrix

- **`shared_nodes/`** - Shared components and utilities
  - State Management nodes (using n8n Context)
  - Error handling and fallback nodes
  - Common utility nodes used across agents

### Organizational Directories

- `exported/` - Production-ready workflow exports from n8n
- `templates/` - Reusable workflow templates

## Multi-Agent System Architecture

This structure enables proper agent routing for the Multi-Agent BRD-to-Engineering System:

1. **BRD Parser** → Cleans and validates input
2. **Planning Agent** → Creates engineering plans and schedules
3. **Design Agent** → Generates architecture and technical documents
4. **Shared Nodes** → Provides state management and error handling

## Usage

1. Build your workflows in the n8n application
2. Export them as JSON files
3. Place the exported JSON files in the appropriate agent directory
4. Use shared nodes for common functionality across agents

### Example File Placement

```
planning_agent/engineering_plan/structured_plan_generator.json
design_agent/architecture/high_level_architecture_generator.json
shared_nodes/state_manager.json
shared_nodes/error_handler.json
```

## Importing Back to n8n

To import a workflow back into n8n:
1. Open n8n application
2. Go to Workflows → Import
3. Select the JSON file from the appropriate directory

