# Complete Project Structure Reference

This document provides a complete reference for the Agent Workflow Based Structure as required by the submission guidelines.

## Full Directory Tree

```
brd_agent_em/
│
├── README.md                                    # Main project documentation
├── STRUCTURE.md                                 # This file - complete structure reference
├── .gitignore                                   # Git ignore rules
│
├── n8n_flows/                                   # ⭐ n8n WORKFLOW FILES (Agent-based structure)
│   │
│   ├── planning_agent/                          # 📋 PLANNING AGENT WORKFLOWS
│   │   ├── README.md                            # Planning agent documentation
│   │   ├── engineering_plan/                    # Structured Engineering Plan workflows
│   │   │   └── structured_plan_generator.json   # (Export from n8n and place here)
│   │   └── project_schedule/                    # Project Schedule workflows
│   │       └── project_schedule_generator.json  # (Export from n8n and place here)
│   │
│   ├── design_agent/                            # 🎨 DESIGN AGENT WORKFLOWS
│   │   ├── README.md                            # Design agent documentation
│   │   ├── architecture/                        # High-Level Architecture workflows
│   │   │   └── architecture_generator.json      # (Export from n8n and place here)
│   │   ├── poc/                                 # Proof of Concept workflows
│   │   │   └── poc_generator.json               # (Export from n8n and place here)
│   │   └── tech_stack/                          # Tech Stack Matrix workflows
│   │       └── tech_stack_generator.json        # (Export from n8n and place here)
│   │
│   ├── shared_nodes/                            # 🔧 SHARED COMPONENTS
│   │   ├── README.md                            # Shared nodes documentation
│   │   ├── state_manager.json                   # State management using n8n Context
│   │   ├── error_handler.json                   # Error handling and fallback logic
│   │   ├── context_reader.json                  # Read from n8n context
│   │   ├── context_writer.json                  # Write to n8n context
│   │   └── validator.json                       # Common validation utilities
│   │
│   ├── exported/                                # Production-ready exports
│   ├── templates/                               # Reusable workflow templates
│   └── README.md                                # n8n flows documentation
│
├── brd_parser/                                  # 📄 BRD PARSER MODULE
│   ├── README.md                                # BRD parser documentation
│   ├── brd_input_cleaner.json                   # ⚠️ MAIN WORKFLOW - place at root level!
│   ├── workflows/                               # Additional workflow files
│   ├── schemas/                                 # JSON validation schemas
│   │   ├── brd_schema.json                      # BRD structure schema
│   │   └── validation_rules.json                # Validation rules
│   └── utils/                                   # Helper scripts
│       ├── text_cleaner.py                      # Text cleaning utilities
│       └── parser_helpers.py                    # Parsing helper functions
│
├── frontend/                                    # 🌐 FRONTEND APPLICATION
│   ├── README.md                                # Frontend documentation
│   ├── src/                                     # Source code
│   │   ├── App.js                               # Main application component
│   │   ├── index.js                             # Entry point
│   │   └── api/                                 # API integration
│   ├── public/                                  # Static assets
│   │   ├── index.html
│   │   └── assets/                              # Images, fonts, etc.
│   └── components/                              # Reusable UI components
│       ├── BRDUploader.js                       # BRD upload component
│       ├── WorkflowViewer.js                    # Workflow visualization
│       └── ResultsDisplay.js                    # Results display component
│
├── sample_inputs/                               # 📁 SAMPLE DATA & TEST INPUTS
│   ├── README.md                                # Sample inputs documentation
│   ├── brds/                                    # Sample BRD documents
│   │   ├── sample_brd_1.pdf                     # Sample BRD 1
│   │   ├── sample_brd_2.docx                    # Sample BRD 2
│   │   └── sample_brd_3.txt                     # Sample BRD 3 (plain text)
│   └── examples/                                # Example input files
│       ├── example_structured_input.json        # Pre-structured example
│       └── example_raw_input.txt                # Raw text example
│
├── tests/                                       # 🧪 TEST SUITES
│   ├── README.md                                # Testing documentation
│   ├── unit/                                    # Unit tests
│   │   ├── test_brd_parser.py                   # BRD parser unit tests
│   │   ├── test_validators.py                   # Validation tests
│   │   └── test_utilities.py                    # Utility function tests
│   └── integration/                             # Integration tests
│       ├── test_planning_agent.py               # Planning agent integration tests
│       ├── test_design_agent.py                 # Design agent integration tests
│       └── test_end_to_end.py                   # End-to-end workflow tests
│
├── docs/                                        # 📚 PROJECT DOCUMENTATION
│   ├── README.md                                # Documentation index
│   ├── architecture.md                          # System architecture overview
│   ├── workflows.md                             # n8n workflow documentation
│   ├── api.md                                   # API documentation
│   ├── deployment.md                            # Deployment instructions
│   ├── user_guide.md                            # User guide
│   └── development.md                           # Development setup guide
│
└── config/                                      # ⚙️ CONFIGURATION FILES
    ├── n8n_config.json                          # n8n configuration
    ├── environment.example.env                  # Example environment variables
    └── deployment_config.yaml                   # Deployment configuration

```

## Critical Requirements

### 1. BRD Parser Placement ⚠️
The main BRD parser workflow **MUST** be placed at:
```
brd_parser/brd_input_cleaner.json
```
**NOT** in a subdirectory like `brd_parser/workflows/brd_input_cleaner.json`

### 2. Agent Workflow Organization
The `n8n_flows/` directory **MUST** contain these three subdirectories:
- `planning_agent/` - For engineering plans and project schedules
- `design_agent/` - For architecture, PoC, and tech stack
- `shared_nodes/` - For state management and error handling

### 3. Five Core Agent Functions
Your system should implement these five functions across the agents:

**Planning Agent (2 functions):**
1. Structured Engineering Plan Generator
2. Project Schedule Generator

**Design Agent (3 functions):**
3. High-Level Architecture Generator
4. Proof of Concept Generator
5. Tech Stack Matrix Generator

### 4. Shared Nodes Requirements
The `shared_nodes/` directory must include:
- **State Management**: Using n8n Context for managing workflow state
- **Error Handling**: Fallback handling for robust operation
- **Common Utilities**: Reusable components across agents

## Development Phases

### Phase 1: MVP (BRD Parser)
✅ Focus on `brd_parser/brd_input_cleaner.json`
✅ Implement basic error handling in `shared_nodes/`
✅ Test with sample inputs

### Phase 2: Planning Agent
✅ Build engineering plan generator
✅ Build project schedule generator
✅ Integrate with BRD parser

### Phase 3: Design Agent
✅ Build architecture generator
✅ Build PoC generator
✅ Build tech stack generator
✅ Integrate with planning agent

### Phase 4: Full Integration
✅ Complete state management system
✅ Comprehensive error handling
✅ Frontend integration
✅ End-to-end testing

## Workflow Data Flow

```
[BRD Input]
    ↓
[BRD Parser] → brd_input_cleaner.json
    ↓
[Shared State Management] ← n8n Context
    ↓
    ├─→ [Planning Agent]
    │       ├─→ Engineering Plan Generator
    │       └─→ Project Schedule Generator
    │
    └─→ [Design Agent]
            ├─→ Architecture Generator
            ├─→ PoC Generator
            └─→ Tech Stack Generator
                    ↓
            [Final Deliverables]
```

## File Naming Conventions

### n8n Workflow Files
- Use descriptive snake_case names
- Include the agent type in the name
- Example: `structured_plan_generator.json`

### Documentation Files
- Use lowercase with underscores or hyphens
- Example: `user_guide.md` or `api-documentation.md`

### Python/JavaScript Files
- Follow language conventions (PEP 8 for Python, etc.)
- Use descriptive names indicating purpose

## Notes for Final Submission

1. ✅ Ensure `brd_input_cleaner.json` is at `brd_parser/` root
2. ✅ All agent workflows are properly organized in `n8n_flows/`
3. ✅ State management and error handling are implemented in `shared_nodes/`
4. ✅ Sample inputs are provided in `sample_inputs/brds/`
5. ✅ Tests cover all major functionality
6. ✅ Documentation is complete and up-to-date
7. ✅ Frontend provides clear user interface
8. ✅ All README files explain their respective modules

