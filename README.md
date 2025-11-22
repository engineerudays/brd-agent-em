# 🤖 BRD Agent - Multi-Agent Engineering Manager

An AI-powered multi-agent system that transforms Business Requirements Documents (BRDs) into comprehensive engineering artifacts including engineering plans, project schedules, architecture designs, and proof-of-concept code.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 What Does It Do?

BRD Agent automates the tedious process of converting business requirements into actionable engineering deliverables:

**Input:** Business Requirements Document (BRD) in **PDF** or **JSON** format

**Output:**
- 📋 **Engineering Plan** - Detailed feature breakdown, technical architecture, implementation phases
- 📅 **Project Schedule** - Timeline, milestones, task assignments, resource allocation
- 📊 **Interactive Gantt Chart** - Visual project timeline
- ⚠️ **Risk Analysis** - Identified risks with mitigation strategies
- 👥 **Resource Requirements** - Team composition and technology stack
- 🏗️ **Architecture Design** - System diagrams, component specifications (Coming Soon)
- 💻 **Proof-of-Concept Code** - Starter implementation (Coming Soon)

---

## ✨ Features

### ✅ Currently Implemented

- **🎨 Streamlit UI**: Beautiful, interactive web interface
- **📄 PDF Upload Support**: Upload BRDs in PDF format with automatic parsing
- **🔍 BRD Parser**: FastAPI service that extracts structured data from BRDs
- **📋 Engineering Plan Generator**: Creates detailed engineering specifications with AI
- **📅 Project Schedule Generator**: Builds comprehensive project timelines
- **📊 Interactive Gantt Chart**: Visual timeline with phases and milestones
- **🎭 Master Orchestrator**: Coordinates all agents in a seamless pipeline
- **🔄 Auto-Retry Logic**: Automatic retry with exponential backoff (3 attempts)
- **💬 Toast Notifications**: Real-time user feedback
- **🧪 Automated Testing**: End-to-end test suite for validation
- **🐳 Docker Support**: Containerized deployment with Docker Compose
- **🔄 n8n Workflows**: Visual workflow automation platform
- **📚 Comprehensive Docs**: User guide, API reference, setup instructions

### 🚧 Coming Soon

- **Architecture Design Agent**: Generate system architecture diagrams
- **Tech Stack Agent**: Recommend and justify technology choices
- **PoC Generator**: Create working proof-of-concept code
- **Session Persistence**: Save/load workspace
- **Batch Processing**: Process multiple BRDs in queue

---

## 📚 Documentation

Comprehensive guides for different audiences:

| Document | Audience | Description |
|----------|----------|-------------|
| **[USER_GUIDE.md](USER_GUIDE.md)** | End Users | Complete usage guide with PDF support, input methods, troubleshooting |
| **[API_REFERENCE.md](API_REFERENCE.md)** | Developers | API endpoints, schemas, architecture, integration guide |
| **[SETUP.md](SETUP.md)** | DevOps/Admins | Installation, configuration, deployment instructions |
| **[README.md](README.md)** | Everyone | Project overview, quick start, features |

**Quick Links:**
- 🎯 [Getting Started](SETUP.md#quick-start)
- 📖 [How to Use](USER_GUIDE.md#getting-started)
- 🔌 [API Reference](API_REFERENCE.md#api-endpoints)
- 🛠️ [Troubleshooting](USER_GUIDE.md#troubleshooting)

---

## 🏗️ Architecture

```
                    ┌─────────────────────────────────┐
                    │     Master Orchestrator         │
                    │      (n8n Workflow)             │
                    └────────────┬────────────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
          ▼                      ▼                      ▼
   ┌──────────┐          ┌──────────┐          ┌──────────┐
   │   BRD    │          │ Planning │          │  Design  │
   │  Parser  │          │  Agent   │          │  Agent   │
   │ (FastAPI)│          │  (n8n)   │          │  (n8n)   │
   └──────────┘          └──────────┘          └──────────┘
        │                      │                      │
        │                      ├──────────────┬──────┤
        │                      │              │      │
        ▼                      ▼              ▼      ▼
   ┌─────────┐        ┌─────────────┐  ┌─────────┐ ...
   │ Parsed  │        │ Engineering │  │ Project │
   │   BRD   │        │    Plan     │  │Schedule │
   └─────────┘        └─────────────┘  └─────────┘
```

### Technology Stack

- **Frontend**: Streamlit (Python)
- **Backend**: Python FastAPI
- **Workflow Engine**: n8n (low-code workflow automation)
- **AI**: Anthropic Claude (Haiku & Sonnet models)
- **Visualization**: Plotly (Interactive Gantt charts)
- **Containerization**: Docker & Docker Compose
- **Testing**: Bash scripts with curl & jq

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Anthropic API Key
- 8GB RAM minimum

### Installation (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/engineerudays/brd-agent-em.git
cd brd-agent-em

# 2. Configure API key
echo "ANTHROPIC_API_KEY=your_key_here" > brd_parser/.env

# 3. Update volume path in docker-compose.yml
# (Replace with your local path)

# 4. Start services
docker-compose up -d

# 5. Import n8n workflows
# Open http://localhost:5678 and import workflows from n8n_flows/

# 6. Test the system
./tests/integration/test_e2e_orchestrator.sh sample_inputs/brds/brd_input_cleaner.json
```

📖 **For detailed setup instructions, see [SETUP.md](SETUP.md)**

---

## 📝 Usage Example

### Input BRD (JSON)

```json
{
  "project": {
    "name": "Customer Onboarding Portal",
    "description": "A portal to streamline customer onboarding",
    "objectives": ["Reduce churn", "Improve TTV"]
  },
  "features": [
    {
      "id": "F001",
      "name": "Single Sign-On",
      "priority": "Critical"
    }
  ]
}
```

### Generated Engineering Plan

```json
{
  "engineering_plan": {
    "project_overview": {...},
    "feature_breakdown": [
      {
        "feature_id": "F-01",
        "complexity": "Medium",
        "estimated_effort": "2 weeks",
        "technical_requirements": [...],
        "acceptance_criteria": [...]
      }
    ],
    "technical_architecture": {...},
    "implementation_phases": [...],
    "risk_analysis": [...],
    "resource_requirements": {...}
  }
}
```

### Generated Project Schedule

```json
{
  "project_schedule": {
    "project_info": {
      "total_duration_weeks": 24,
      "start_date": "2025-01-01"
    },
    "phases": [...],
    "resource_allocation": [...],
    "critical_path": [...],
    "key_deliverables": [...]
  }
}
```

---

## 📊 Project Status

| Component | Status | Completion |
|-----------|--------|------------|
| BRD Parser | ✅ Complete | 100% |
| Engineering Plan Generator | ✅ Complete | 100% |
| Project Schedule Generator | ✅ Complete | 100% |
| Master Orchestrator | ✅ Complete | 100% |
| Architecture Design Agent | 🚧 Planned | 0% |
| Tech Stack Agent | 🚧 Planned | 0% |
| PoC Generator | 🚧 Planned | 0% |
| Streamlit Frontend | 🚧 Planned | 0% |

---

## 🗂️ Repository Structure

```
brd_agent_em/
├── brd_parser/                 # FastAPI BRD Parser Service
│   ├── main.py                # Parser implementation
│   ├── Dockerfile
│   └── README.md
├── n8n_flows/                 # n8n Workflow Definitions
│   ├── master_orchestrator.json
│   ├── planning_agent/
│   │   ├── engineering_plan/
│   │   └── project_schedule/
│   └── design_agent/          # Coming soon
├── sample_inputs/             # Test data
│   ├── brds/                  # Sample BRD files
│   └── outputs/               # Generated artifacts (ignored by git)
├── tests/integration/         # Automated tests
│   ├── test_e2e_orchestrator.sh
│   └── README.md
├── docker-compose.yml         # Service orchestration
├── README.md                  # This file
└── SETUP.md                   # Detailed setup guide
```

---

## 🧪 Testing

Run the automated end-to-end test:

```bash
./tests/integration/test_e2e_orchestrator.sh sample_inputs/brds/brd_input_cleaner.json
```

**Expected Output:**
```
✓ END-TO-END TEST PASSED!
```

---

## 🤝 Contributing

This is a personal project for learning and demonstration. Feel free to:
- Fork and experiment
- Submit issues for bugs
- Suggest improvements

---

## 📜 License

MIT License - Feel free to use this project for learning and inspiration.

---

## 🙏 Acknowledgments

- **n8n** - Low-code workflow automation platform
- **Anthropic** - Claude AI models for intelligent content generation
- **FastAPI** - Modern Python web framework

---

## 📧 Contact

**Author**: Uday Ammanagi  
**GitHub**: [@engineerudays](https://github.com/engineerudays)

---

## 🎯 Roadmap

### Phase 1: Planning Agent (✅ Complete)
- [x] BRD Parser
- [x] Engineering Plan Generator
- [x] Project Schedule Generator
- [x] Master Orchestrator
- [x] End-to-end testing

### Phase 2: Design Agent (🚧 In Progress)
- [ ] Architecture Design Generator
- [ ] Tech Stack Recommender
- [ ] PoC Code Generator

### Phase 3: Frontend (🔜 Planned)
- [ ] Streamlit web interface
- [ ] BRD upload functionality
- [ ] Output visualization
- [ ] PDF export

### Phase 4: Enhancements (💡 Future)
- [ ] Support for PDF BRD input
- [ ] Multi-language support
- [ ] Custom templates
- [ ] Version control for artifacts

---

**⭐ If you find this project interesting, please star the repository!**

**📖 Get started with the [SETUP.md](SETUP.md) guide.**
