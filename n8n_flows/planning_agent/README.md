# Planning Agent Workflows

This directory contains n8n workflows for the Planning Agent, responsible for generating engineering plans and project schedules.

## Structure

- **`engineering_plan/`** - Workflows for generating Structured Engineering Plans
- **`project_schedule/`** - Workflows for generating Project Schedules

## Planning Agent Functions

### 1. Structured Engineering Plan Generator
- Takes parsed BRD as input
- Generates comprehensive engineering plan
- Includes feature breakdown, technical requirements, dependencies
- Output: Structured engineering plan document

### 2. Project Schedule Generator
- Takes engineering plan as input
- Creates detailed project timeline
- Estimates effort and identifies milestones
- Output: Project schedule with timelines and dependencies

## Workflow Files

Place exported n8n workflows here with descriptive names:
- `engineering_plan/structured_plan_generator.json`
- `project_schedule/project_schedule_generator.json`

## Integration Points

- **Input**: Parsed BRD from BRD Parser
- **Output**: Engineering plans and schedules → Design Agent or final output
- **Shared Resources**: Uses shared_nodes for state management and error handling

