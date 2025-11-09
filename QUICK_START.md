# Quick Start Guide

This guide helps you quickly understand where to place your n8n workflow exports.

## 🚀 Quick Reference: Where to Place Your n8n Exports

### Step 1: BRD Parser (MANDATORY for MVP)
After building your BRD Input Parser workflow in n8n:
```bash
Export from n8n → Place at: brd_parser/brd_input_cleaner.json
```
⚠️ **Important**: Place at the ROOT of `brd_parser/`, not in a subdirectory!

### Step 2: Shared Nodes (MANDATORY)
Build and export your state management and error handling nodes:
```bash
Export from n8n → Place in: n8n_flows/shared_nodes/
Examples:
  - state_manager.json
  - error_handler.json
  - context_reader.json
  - context_writer.json
```

### Step 3: Planning Agent (Optional for MVP, Required for Full System)
Build and export Planning Agent workflows:
```bash
Engineering Plan:
  Export from n8n → n8n_flows/planning_agent/engineering_plan/

Project Schedule:
  Export from n8n → n8n_flows/planning_agent/project_schedule/
```

### Step 4: Design Agent (Optional for MVP, Required for Full System)
Build and export Design Agent workflows:
```bash
Architecture:
  Export from n8n → n8n_flows/design_agent/architecture/

PoC Document:
  Export from n8n → n8n_flows/design_agent/poc/

Tech Stack:
  Export from n8n → n8n_flows/design_agent/tech_stack/
```

## 📋 MVP Checklist (Minimum Viable Product)

- [ ] Install and set up n8n
- [ ] Build **BRD Input Parser** workflow in n8n
- [ ] Export and place at `brd_parser/brd_input_cleaner.json`
- [ ] Build **State Management** nodes
- [ ] Build **Error Handling** nodes  
- [ ] Export shared nodes to `n8n_flows/shared_nodes/`
- [ ] Add sample BRD files to `sample_inputs/brds/`
- [ ] Test the parser with sample inputs
- [ ] Write basic tests in `tests/unit/`

## 🎯 Full System Checklist

After completing MVP, build the complete multi-agent system:

**Planning Agent:**
- [ ] Build Structured Engineering Plan Generator
- [ ] Build Project Schedule Generator
- [ ] Export to `n8n_flows/planning_agent/`

**Design Agent:**
- [ ] Build High-Level Architecture Generator
- [ ] Build PoC Document Generator
- [ ] Build Tech Stack Matrix Generator
- [ ] Export to `n8n_flows/design_agent/`

**Integration:**
- [ ] Connect BRD Parser → Planning Agent
- [ ] Connect BRD Parser → Design Agent
- [ ] Implement state management across agents
- [ ] Add comprehensive error handling
- [ ] Build frontend interface
- [ ] Write integration tests

## 🔧 Common n8n Export Steps

1. **Open your workflow** in n8n
2. **Click the menu** (three dots) in the top right
3. **Select "Download"** or "Export"
4. **Save the .json file** to the appropriate directory based on this guide
5. **Commit to version control**

## 📁 Directory Quick Reference

| Component | Location | Purpose |
|-----------|----------|---------|
| BRD Parser | `brd_parser/brd_input_cleaner.json` | Entry point, cleans BRD input |
| Planning - Engineering Plan | `n8n_flows/planning_agent/engineering_plan/` | Generates engineering plans |
| Planning - Project Schedule | `n8n_flows/planning_agent/project_schedule/` | Generates project schedules |
| Design - Architecture | `n8n_flows/design_agent/architecture/` | Generates architecture docs |
| Design - PoC | `n8n_flows/design_agent/poc/` | Generates PoC documents |
| Design - Tech Stack | `n8n_flows/design_agent/tech_stack/` | Generates tech recommendations |
| Shared Nodes | `n8n_flows/shared_nodes/` | State management & error handling |
| Sample BRDs | `sample_inputs/brds/` | Test BRD documents |
| Tests | `tests/unit/` & `tests/integration/` | Test suites |

## 🎨 Frontend Setup (Optional)

If building a frontend:
```bash
cd frontend/
npm init react-app .
# or
npm init vue@latest .
```

Place your components in `frontend/components/` and source code in `frontend/src/`.

## 🧪 Testing Your Setup

1. Add a sample BRD to `sample_inputs/brds/`
2. Import `brd_input_cleaner.json` back into n8n
3. Run the workflow with your sample BRD
4. Verify output and error handling
5. Write tests based on expected behavior

## 📚 Need More Details?

- **Complete structure**: See `STRUCTURE.md`
- **Project overview**: See `README.md`
- **Module-specific docs**: See `README.md` in each directory
- **Agent workflows**: See `n8n_flows/*/README.md`

## ⚠️ Submission Requirements Checklist

Before final submission, ensure:

- [ ] `brd_input_cleaner.json` is at `brd_parser/` root (not in subdirectory)
- [ ] All five agent functions are implemented
- [ ] `shared_nodes/` contains state management and error handling
- [ ] Sample inputs are provided
- [ ] Tests are written and passing
- [ ] Documentation is complete
- [ ] All README files are updated
- [ ] .gitignore is properly configured

## 💡 Pro Tips

1. **Start with MVP**: Get the BRD parser working first before building other agents
2. **Test incrementally**: Test each agent independently before integration
3. **Use shared nodes**: Avoid duplicating logic across workflows
4. **Version control**: Commit after each major milestone
5. **Document as you go**: Update README files as you build features
6. **Sample data**: Create diverse sample BRDs to test edge cases

