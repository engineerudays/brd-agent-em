# Shared Nodes

This directory contains reusable n8n workflow components used across multiple agents.

## Purpose

Shared nodes enable:
- **State Management** using n8n Context
- **Error Handling** and fallback mechanisms
- **Common Utilities** used by multiple agents
- **Code Reusability** across workflows

## Critical Components

### 1. State Management Nodes
- Manage workflow state using n8n Context
- Store and retrieve intermediate results
- Enable data flow between agents
- Maintain system state across workflow executions

**Example workflows:**
- `state_manager.json` - Core state management logic
- `context_reader.json` - Read from n8n context
- `context_writer.json` - Write to n8n context

### 2. Error Handling Nodes
- Implement fallback handling for failures
- Log errors and warnings
- Retry mechanisms for transient failures
- Graceful degradation strategies

**Example workflows:**
- `error_handler.json` - Central error handling logic
- `fallback_handler.json` - Fallback mechanisms
- `retry_logic.json` - Retry with exponential backoff

### 3. Common Utility Nodes
- Data transformation utilities
- Validation helpers
- Formatting functions
- API integration helpers

**Example workflows:**
- `data_transformer.json` - Common data transformations
- `validator.json` - Input validation logic
- `formatter.json` - Output formatting utilities

## Usage in Agent Workflows

Import shared nodes into your agent workflows:

1. **In n8n**: Use "Link to Workflow" or "Execute Workflow" nodes
2. **Reference shared nodes** from planning_agent and design_agent workflows
3. **Maintain consistency** by updating shared nodes rather than duplicating logic

## Best Practices

- Keep shared nodes generic and reusable
- Document inputs and outputs clearly
- Version control shared nodes carefully
- Test shared nodes independently before integration

