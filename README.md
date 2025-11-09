# brd_agent_em - Agent Workflow Structure

This project uses n8n for agent orchestration with a modular workflow-based architecture.

## Project Structure

```
brd_agent_em/
├── n8n_flows/                          # n8n Workflow JSON files (Agent-based structure)
│   ├── planning_agent/                 # Planning Agent workflows
│   │   ├── engineering_plan/          # Structured Engineering Plan generator
│   │   └── project_schedule/          # Project Schedule generator
│   ├── design_agent/                   # Design Agent workflows
│   │   ├── architecture/               # High-Level Architecture generator
│   │   ├── poc/                        # Proof of Concept generator
│   │   └── tech_stack/                 # Tech Stack Matrix generator
│   ├── shared_nodes/                   # Shared components (State Management, Error Handling)
│   ├── exported/                       # Production-ready exported flows
│   └── templates/                      # Template flows for reuse
│
├── brd_parser/                         # BRD (Business Requirements Document) Parser
│   ├── brd_input_cleaner.json         # ⚠️ Main parser workflow (place here for final submission)
│   ├── workflows/                      # Additional BRD parser workflow files
│   ├── schemas/                        # JSON schemas for BRD validation
│   └── utils/                          # Utility scripts for parsing
│
├── frontend/                           # Frontend application
│   ├── src/                            # Source code
│   ├── public/                         # Public assets
│   └── components/                     # React/Vue components
│
├── sample_inputs/                      # Sample data and test inputs
│   ├── brds/                           # Sample BRD documents
│   └── examples/                       # Example input files
│
├── tests/                              # Test suites
│   ├── unit/                           # Unit tests
│   └── integration/                    # Integration tests
│
├── docs/                               # Project documentation
│
└── config/                             # Configuration files

```

## Multi-Agent System Architecture

This project implements a **Multi-Agent BRD-to-Engineering System** with three core components:

1. **BRD Parser Agent** - Entry point that cleans and validates BRD input
2. **Planning Agent** - Generates engineering plans and project schedules
3. **Design Agent** - Creates architecture, PoC documents, and tech stack recommendations
4. **Shared Components** - State management and error handling across all agents

## Workflow

1. **Design flows in n8n:** Use the n8n graphical interface to build your workflows
2. **Export flows:** Save/export workflows as JSON files from n8n
3. **Place in structure:** Move exported JSON files to appropriate agent folders

### Agent Workflow Placement

- **BRD Parser**: `brd_parser/brd_input_cleaner.json` (root of brd_parser/)
- **Planning Agent**: `n8n_flows/planning_agent/[engineering_plan|project_schedule]/`
- **Design Agent**: `n8n_flows/design_agent/[architecture|poc|tech_stack]/`
- **Shared Nodes**: `n8n_flows/shared_nodes/`

## Getting Started

### MVP (Minimum Viable Product)
1. Set up n8n application
2. Create your **BRD Input Parser** workflow in n8n
3. Export the workflow and save it to `brd_parser/brd_input_cleaner.json`
4. Create **shared nodes** for state management and error handling
5. Add sample BRD documents to `sample_inputs/brds/`
6. Write tests in the `tests/` directory

### Full Multi-Agent System
1. Build Planning Agent workflows (engineering plan + project schedule)
2. Build Design Agent workflows (architecture + PoC + tech stack)
3. Integrate all agents using shared state management
4. Implement error handling and fallback mechanisms
5. Build frontend for user interaction
6. Add comprehensive tests

## Key Files

- `brd_parser/brd_input_cleaner.json` - **Main BRD parser workflow** ⚠️ Required at root
- `n8n_flows/planning_agent/` - Planning Agent workflows
- `n8n_flows/design_agent/` - Design Agent workflows
- `n8n_flows/shared_nodes/` - State management and error handling
- `sample_inputs/brds/` - Sample BRD documents for testing
- `tests/` - Test cases for validation

## Notes

- This structure ensures modularity and easy debugging
- Each workflow should be self-contained and well-documented
- Follow the submission guidelines for proper organization

