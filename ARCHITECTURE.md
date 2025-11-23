# 🏗️ BRD Agent - System Architecture

## 📊 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE LAYER                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Streamlit Web UI (Port 8501) ✅ IMPLEMENTED                        │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │  • PDF Upload Support         • Interactive Gantt Charts            │   │
│  │  • JSON Input (Paste/Upload)  • Human-Readable Displays             │   │
│  │  • Sample BRD Library         • Download Artifacts                  │   │
│  │  • Real-time Status Updates   • Toast Notifications                 │   │
│  │  • Retry Logic (Exponential)  • Error Handling & Debug Info         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                  │                                            │
│                                  │ HTTP POST (JSON)                           │
│                                  ▼                                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATION LAYER (n8n)                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Master Orchestrator ✅ IMPLEMENTED                                 │   │
│  │  Webhook: /webhook/orchestrator/process-brd-v2                      │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │  1. Receive BRD Input (PDF/JSON)                                    │   │
│  │  2. Route to BRD Parser (if PDF)                                    │   │
│  │  3. Call Planning Agent Workflows                                   │   │
│  │  4. Call Design Agent Workflows (TODO)                              │   │
│  │  5. Aggregate & Return Results                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                          │                        │                │
│         │                          │                        │                │
│         ▼                          ▼                        ▼                │
│   ┌──────────┐            ┌──────────────┐        ┌──────────────┐         │
│   │   BRD    │            │   PLANNING   │        │   DESIGN     │         │
│   │  Parser  │            │    AGENT     │        │    AGENT     │         │
│   │    ✅    │            │      ✅      │        │     ⏸️       │         │
│   └──────────┘            └──────────────┘        └──────────────┘         │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         AGENT SERVICES LAYER                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  📄 BRD PARSER SERVICE (FastAPI) ✅ IMPLEMENTED                    │    │
│  │  Port: 8000 | Docker Container                                     │    │
│  ├────────────────────────────────────────────────────────────────────┤    │
│  │  • PDF Text Extraction (PyPDF2)                                    │    │
│  │  • AI-Powered Structured Extraction (Claude 3 Haiku)              │    │
│  │  • JSON Validation & Formatting                                    │    │
│  │  • Health Check Endpoint                                           │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  🎯 PLANNING AGENT (n8n Workflows) ✅ IMPLEMENTED                  │    │
│  │  Webhooks: /webhook/planning-agent/*                               │    │
│  ├────────────────────────────────────────────────────────────────────┤    │
│  │                                                                     │    │
│  │  ┌──────────────────────────────────────────────────────────┐     │    │
│  │  │  Engineering Plan Generator ✅                           │     │    │
│  │  │  /webhook/planning-agent/engineering-plan                │     │    │
│  │  ├──────────────────────────────────────────────────────────┤     │    │
│  │  │  Input:  Raw BRD JSON                                    │     │    │
│  │  │  AI:     Claude 3 Haiku (4096 tokens)                    │     │    │
│  │  │  Output: • Project Overview                              │     │    │
│  │  │          • Feature Breakdown (priorities, complexity)    │     │    │
│  │  │          • Technical Architecture                        │     │    │
│  │  │          • Implementation Phases                         │     │    │
│  │  │          • Risk Analysis                                 │     │    │
│  │  │          • Resource Requirements                         │     │    │
│  │  │          • Success Metrics                               │     │    │
│  │  │  Saves:  engineering_plans/*.json (versioned)            │     │    │
│  │  └──────────────────────────────────────────────────────────┘     │    │
│  │                                                                     │    │
│  │  ┌──────────────────────────────────────────────────────────┐     │    │
│  │  │  Project Schedule Generator ✅                           │     │    │
│  │  │  /webhook/planning-agent/project-schedule                │     │    │
│  │  ├──────────────────────────────────────────────────────────┤     │    │
│  │  │  Input:  Engineering Plan JSON                           │     │    │
│  │  │  AI:     Claude 3 Haiku (4096 tokens)                    │     │    │
│  │  │  Output: • Project Timeline (dates, durations)           │     │    │
│  │  │          • Phases & Tasks (detailed breakdown)           │     │    │
│  │  │          • Resource Allocation                           │     │    │
│  │  │          • Critical Path Analysis                        │     │    │
│  │  │          • Risk Timeline                                 │     │    │
│  │  │          • Key Deliverables                              │     │    │
│  │  │          • Milestones                                    │     │    │
│  │  │  Saves:  project_schedules/*.json (versioned)            │     │    │
│  │  └──────────────────────────────────────────────────────────┘     │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  🎨 DESIGN AGENT (n8n Workflows) ⏸️ TODO                           │    │
│  │  Webhooks: /webhook/design-agent/*                                 │    │
│  ├────────────────────────────────────────────────────────────────────┤    │
│  │                                                                     │    │
│  │  ┌──────────────────────────────────────────────────────────┐     │    │
│  │  │  Architecture Designer ⏸️ TODO                           │     │    │
│  │  │  /webhook/design-agent/architecture                      │     │    │
│  │  ├──────────────────────────────────────────────────────────┤     │    │
│  │  │  Input:  BRD + Engineering Plan                          │     │    │
│  │  │  Output: • System Architecture Diagram (Mermaid/PlantUML)│     │    │
│  │  │          • Component Specifications                      │     │    │
│  │  │          • Technology Stack Recommendations              │     │    │
│  │  │          • Integration Patterns                          │     │    │
│  │  │          • Security Architecture                         │     │    │
│  │  └──────────────────────────────────────────────────────────┘     │    │
│  │                                                                     │    │
│  │  ┌──────────────────────────────────────────────────────────┐     │    │
│  │  │  PoC Generator ⏸️ TODO                                   │     │    │
│  │  │  /webhook/design-agent/poc                               │     │    │
│  │  ├──────────────────────────────────────────────────────────┤     │    │
│  │  │  Input:  Architecture + Feature Breakdown                │     │    │
│  │  │  Output: • Proof of Concept Code                         │     │    │
│  │  │          • Setup Instructions                            │     │    │
│  │  │          • Demo Scripts                                  │     │    │
│  │  │          • Testing Guidelines                            │     │    │
│  │  └──────────────────────────────────────────────────────────┘     │    │
│  │                                                                     │    │
│  │  ┌──────────────────────────────────────────────────────────┐     │    │
│  │  │  Tech Stack Advisor ⏸️ TODO                              │     │    │
│  │  │  /webhook/design-agent/tech-stack                        │     │    │
│  │  ├──────────────────────────────────────────────────────────┤     │    │
│  │  │  Input:  Requirements + Constraints                      │     │    │
│  │  │  Output: • Framework Recommendations                     │     │    │
│  │  │          • Database Selection                            │     │    │
│  │  │          • Infrastructure Choices                        │     │    │
│  │  │          • Third-party Services                          │     │    │
│  │  │          • Cost Analysis                                 │     │    │
│  │  └──────────────────────────────────────────────────────────┘     │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         AI/ML SERVICES LAYER                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  🤖 Anthropic Claude API ✅ ACTIVE                                 │    │
│  │  https://api.anthropic.com/v1/messages                             │    │
│  ├────────────────────────────────────────────────────────────────────┤    │
│  │  Models in Use:                                                    │    │
│  │  • Claude 3 Haiku (fast, cost-effective)                           │    │
│  │  • Max Tokens: 4096 per response                                   │    │
│  │  • Rate Limit: 50,000 input tokens/minute (Free Tier)             │    │
│  │                                                                     │    │
│  │  Usage:                                                            │    │
│  │  • BRD Parser: ~2,000 tokens/call                                  │    │
│  │  • Engineering Plan: ~8,000 tokens/call                            │    │
│  │  • Project Schedule: ~12,000 tokens/call                           │    │
│  │  • Total per run: ~20,000 tokens (2.5 runs/minute)                │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      DATA PERSISTENCE LAYER                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  📁 File System Storage ✅ IMPLEMENTED                             │    │
│  │  Location: /Users/.../IK/brd_agent_em/sample_inputs/outputs/       │    │
│  ├────────────────────────────────────────────────────────────────────┤    │
│  │  Structure:                                                        │    │
│  │  ├── engineering_plans/                                            │    │
│  │  │   └── engineering_plan_{project}_v{n}_{timestamp}.json          │    │
│  │  ├── project_schedules/                                            │    │
│  │  │   └── project_schedule_{project}_v{n}_{timestamp}.json          │    │
│  │  ├── architectures/         ⏸️ TODO                                │    │
│  │  ├── pocs/                  ⏸️ TODO                                │    │
│  │  └── tech_stacks/           ⏸️ TODO                                │    │
│  │                                                                     │    │
│  │  Features:                                                         │    │
│  │  • Automatic versioning (v1, v2, ...)                              │    │
│  │  • Timestamped filenames                                           │    │
│  │  • Human-readable JSON (pretty-printed)                            │    │
│  │  • Docker volume mounted                                           │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  🗄️ Database (Future) ⏸️ TODO                                      │    │
│  ├────────────────────────────────────────────────────────────────────┤    │
│  │  • Project Metadata Storage                                        │    │
│  │  • User Management                                                 │    │
│  │  • Audit Logs                                                      │    │
│  │  • Version History Tracking                                        │    │
│  │  • Search & Analytics                                              │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      INFRASTRUCTURE LAYER                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  🐳 Docker Compose ✅ IMPLEMENTED                                  │    │
│  ├────────────────────────────────────────────────────────────────────┤    │
│  │                                                                     │    │
│  │  Services:                                                         │    │
│  │  ┌─────────────────────────────────────────────────────────┐      │    │
│  │  │  n8n (Workflow Engine)                                  │      │    │
│  │  │  • Port: 5678                                           │      │    │
│  │  │  • Volume: n8n_data (workflows, credentials, state)     │      │    │
│  │  │  • Volume: /data/projects (host filesystem mount)       │      │    │
│  │  │  • Network: n8n-network                                 │      │    │
│  │  └─────────────────────────────────────────────────────────┘      │    │
│  │                                                                     │    │
│  │  ┌─────────────────────────────────────────────────────────┐      │    │
│  │  │  brd-parser (FastAPI Service)                           │      │    │
│  │  │  • Port: 8000                                           │      │    │
│  │  │  • Health: /health                                      │      │    │
│  │  │  • Network: n8n-network                                 │      │    │
│  │  │  • Env: .env (ANTHROPIC_API_KEY)                        │      │    │
│  │  └─────────────────────────────────────────────────────────┘      │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  🖥️ Local Development ✅ ACTIVE                                    │    │
│  ├────────────────────────────────────────────────────────────────────┤    │
│  │  • Streamlit: Python 3.x, local venv                               │    │
│  │  • Port: 8501 (not containerized)                                  │    │
│  │  • Dependencies: requirements.txt                                  │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Diagram

```
┌──────────┐
│   USER   │
└────┬─────┘
     │
     │ 1. Upload BRD (PDF/JSON)
     ▼
┌─────────────────┐
│  Streamlit UI   │
│   (Port 8501)   │
└────┬────────────┘
     │
     │ 2. HTTP POST /webhook/orchestrator/process-brd-v2
     ▼
┌──────────────────────┐
│  Master Orchestrator │
│    (n8n Workflow)    │
└──┬──────┬────────┬───┘
   │      │        │
   │      │        │ 3a. If PDF → Parse
   │      │        ▼
   │      │   ┌──────────────┐
   │      │   │  BRD Parser  │──── Anthropic Claude
   │      │   │   (FastAPI)  │     (Extract Structure)
   │      │   └──────┬───────┘
   │      │          │
   │      │          │ Structured JSON
   │      │          ▼
   │      │   4. Generate Engineering Plan
   │      │          │
   │      ▼          ▼
   │   ┌────────────────────────┐
   │   │ Engineering Plan Gen   │──── Anthropic Claude
   │   │   (n8n Workflow)       │     (Generate Plan)
   │   └────────┬───────────────┘
   │            │
   │            │ Engineering Plan JSON
   │            │ + Save to File
   │            ▼
   │   5. Generate Project Schedule
   │            │
   ▼            ▼
┌────────────────────────────┐
│  Project Schedule Gen      │──── Anthropic Claude
│    (n8n Workflow)          │     (Generate Timeline)
└──────────┬─────────────────┘
           │
           │ Project Schedule JSON
           │ + Save to File
           │
           │ 6. Return Complete Results
           ▼
      ┌─────────────┐
      │ Streamlit UI │
      │   Display    │
      ├─────────────┤
      │ • Engineering Plan (Collapsible)   │
      │ • Project Schedule (Collapsible)   │
      │ • Gantt Chart (Interactive)        │
      │ • Download Options                 │
      └─────────────────────────────────────┘
```

---

## 📦 Technology Stack

### ✅ Implemented

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit 1.28 | Web UI |
| **Orchestration** | n8n (Docker) | Workflow automation |
| **AI/ML** | Anthropic Claude 3 Haiku | Natural language processing |
| **Backend Services** | FastAPI + Uvicorn | BRD Parser REST API |
| **PDF Processing** | PyPDF2 | PDF text extraction |
| **Visualization** | Plotly 5.17 | Interactive Gantt charts |
| **Data Tables** | Pandas 2.1 | Data manipulation |
| **Containerization** | Docker + Docker Compose | Service isolation |
| **Version Control** | Git + GitHub | Code management |
| **HTTP Client** | Requests 2.31 | API communication |

### ⏸️ TODO (Future Enhancements)

| Component | Technology (Suggested) | Purpose |
|-----------|----------------------|---------|
| **Database** | PostgreSQL | Project metadata, user management |
| **Caching** | Redis | Performance optimization |
| **Authentication** | OAuth 2.0 / JWT | User authentication |
| **API Gateway** | Kong / Nginx | Rate limiting, routing |
| **Message Queue** | RabbitMQ / Kafka | Async job processing |
| **Monitoring** | Prometheus + Grafana | System health monitoring |
| **Logging** | ELK Stack | Centralized logging |
| **Code Generation** | LangChain + LLM | PoC code generation |
| **Diagram Generation** | Mermaid.js / PlantUML | Architecture diagrams |

---

## 🎯 Implementation Status

### ✅ Completed (100%)

**Core Infrastructure:**
- [x] Docker Compose setup
- [x] n8n workflow engine
- [x] Volume mounting for file persistence
- [x] Network configuration
- [x] Environment variable management

**BRD Parser Service:**
- [x] FastAPI application
- [x] PDF upload & parsing (PyPDF2)
- [x] AI-powered structure extraction (Claude)
- [x] JSON validation & formatting
- [x] Health check endpoint
- [x] Docker containerization
- [x] Error handling

**Planning Agent:**
- [x] Engineering Plan Generator workflow
  - [x] BRD parsing & validation
  - [x] AI prompt engineering (detailed)
  - [x] Full BRD context preservation
  - [x] Comprehensive output structure
  - [x] File saving (versioned)
  - [x] Webhook response handling
- [x] Project Schedule Generator workflow
  - [x] Engineering plan parsing
  - [x] Timeline generation
  - [x] Task breakdown
  - [x] Resource allocation
  - [x] Critical path analysis
  - [x] File saving (versioned)

**Master Orchestrator:**
- [x] BRD input handling (PDF/JSON)
- [x] BRD format normalization
- [x] Workflow chaining
- [x] State management (simplified)
- [x] Error handling
- [x] Response aggregation
- [x] Data extraction & formatting

**Streamlit UI:**
- [x] PDF upload support
- [x] JSON upload support
- [x] JSON paste support
- [x] Sample BRD library
- [x] BRD validation
- [x] Processing orchestration
- [x] Real-time status updates
- [x] Toast notifications
- [x] Retry logic (exponential backoff)
- [x] Human-readable displays
  - [x] Engineering plan (collapsible sections)
  - [x] Project schedule (collapsible sections)
- [x] Interactive Gantt chart (Plotly)
- [x] Download artifacts
- [x] Error handling & debug info
- [x] Session state management
- [x] Configuration management

**Testing & Documentation:**
- [x] End-to-end integration test script
- [x] Individual workflow test scripts
- [x] Tiny test BRD (for development)
- [x] README.md (project overview)
- [x] SETUP.md (complete setup guide)
- [x] USER_GUIDE.md (user documentation)
- [x] API_REFERENCE.md (API & architecture docs)
- [x] Integration test README

---

### ⏸️ TODO (Design Agent - 0%)

**Architecture Designer Workflow:**
- [ ] Workflow creation in n8n
- [ ] Input: BRD + Engineering Plan
- [ ] AI prompt for architecture design
- [ ] System component identification
- [ ] Integration pattern recommendations
- [ ] Security architecture design
- [ ] Mermaid/PlantUML diagram generation
- [ ] File saving (versioned)
- [ ] Webhook integration

**PoC Generator Workflow:**
- [ ] Workflow creation in n8n
- [ ] Input: Architecture + Feature breakdown
- [ ] AI prompt for code generation
- [ ] Multi-file code generation
- [ ] Setup instructions generation
- [ ] Test script generation
- [ ] ZIP file packaging
- [ ] File saving (versioned)
- [ ] Webhook integration

**Tech Stack Advisor Workflow:**
- [ ] Workflow creation in n8n
- [ ] Input: Requirements + Constraints
- [ ] AI prompt for tech recommendations
- [ ] Framework comparison analysis
- [ ] Database selection logic
- [ ] Infrastructure recommendations
- [ ] Cost analysis generation
- [ ] Trade-off documentation
- [ ] File saving (versioned)
- [ ] Webhook integration

**Integration with Master Orchestrator:**
- [ ] Add Design Agent calls to orchestrator
- [ ] Conditional execution (optional Design Agent)
- [ ] State management for design artifacts
- [ ] Response aggregation
- [ ] Error handling

**UI Enhancements for Design Agent:**
- [ ] Architecture diagram viewer
- [ ] Code preview/download
- [ ] Tech stack comparison table
- [ ] Cost analysis visualization

---

### 🔮 Future Enhancements (Not Started)

**Advanced Features:**
- [ ] Multi-user support & authentication
- [ ] Project workspace management
- [ ] Version control integration (Git)
- [ ] Collaborative editing
- [ ] Real-time collaboration
- [ ] Comment system
- [ ] Approval workflows
- [ ] Template library
- [ ] Custom prompt templates
- [ ] Plugin system

**Data & Analytics:**
- [ ] Project dashboard
- [ ] Usage analytics
- [ ] Cost tracking
- [ ] Performance metrics
- [ ] Historical data analysis
- [ ] Export to project management tools (Jira, Asana)
- [ ] Integration with CI/CD pipelines

**Infrastructure Improvements:**
- [ ] Kubernetes deployment
- [ ] Auto-scaling
- [ ] Load balancing
- [ ] CDN integration
- [ ] Backup & disaster recovery
- [ ] Multi-region deployment
- [ ] High availability setup

**AI/ML Enhancements:**
- [ ] Model fine-tuning
- [ ] Custom training data
- [ ] Multi-model support (GPT-4, Gemini)
- [ ] Model performance comparison
- [ ] Feedback loop for improvement
- [ ] Context-aware suggestions
- [ ] Learning from past projects

---

## 🔐 Security Considerations

### ✅ Implemented

- [x] API key management (environment variables)
- [x] Docker network isolation
- [x] HTTPS for external API calls (Anthropic)
- [x] Input validation (BRD JSON schema)
- [x] Error sanitization (no sensitive data in errors)

### ⏸️ TODO

- [ ] User authentication & authorization
- [ ] Role-based access control (RBAC)
- [ ] Audit logging
- [ ] Encryption at rest
- [ ] API rate limiting
- [ ] DDoS protection
- [ ] Security headers (CORS, CSP)
- [ ] Vulnerability scanning
- [ ] Secrets management (HashiCorp Vault)

---

## 📈 Scalability Considerations

### Current Limitations

- **Single instance** of n8n and BRD Parser
- **File-based storage** (not suitable for high concurrency)
- **No caching** (repeated requests hit AI API)
- **Synchronous processing** (blocks during AI calls)
- **Rate limits** (Anthropic free tier: 50K tokens/min)

### Future Improvements

- [ ] **Horizontal scaling** (multiple n8n instances)
- [ ] **Database migration** (PostgreSQL for metadata)
- [ ] **Caching layer** (Redis for frequently accessed data)
- [ ] **Async processing** (message queue for long-running tasks)
- [ ] **Load balancer** (distribute requests)
- [ ] **CDN** (static asset delivery)
- [ ] **Auto-scaling** (Kubernetes HPA)

---

## 📊 Performance Metrics

### Current Performance

| Metric | Value | Notes |
|--------|-------|-------|
| **Full Pipeline** | ~28-30 seconds | Tiny BRD |
| **Full Pipeline** | ~40-50 seconds | Full BRD |
| **Engineering Plan** | ~15-20 seconds | Depends on BRD size |
| **Project Schedule** | ~10-15 seconds | Depends on plan complexity |
| **BRD Parsing** | ~5-10 seconds | PDF → JSON |
| **Token Usage** | ~20,000 tokens/run | Full BRD |
| **Rate Limit** | 2.5 runs/minute | Free tier |

### Performance Optimization TODO

- [ ] Reduce prompt sizes (50% reduction possible)
- [ ] Implement caching (avoid duplicate AI calls)
- [ ] Parallel processing (independent workflows)
- [ ] Streaming responses (partial results)
- [ ] Batch processing (multiple BRDs)

---

## 🎯 Next Milestones

### Phase 1: Design Agent (Priority: High)
**Estimated Effort:** 2-3 weeks

- [ ] Architecture Designer workflow
- [ ] PoC Generator workflow
- [ ] Tech Stack Advisor workflow
- [ ] Integration with Master Orchestrator
- [ ] UI enhancements for Design Agent outputs
- [ ] Testing & documentation

### Phase 2: Production Readiness (Priority: Medium)
**Estimated Effort:** 1-2 weeks

- [ ] Database integration (PostgreSQL)
- [ ] User authentication
- [ ] API rate limiting
- [ ] Monitoring & logging
- [ ] Backup & recovery
- [ ] Production deployment guide

### Phase 3: Advanced Features (Priority: Low)
**Estimated Effort:** 4-6 weeks

- [ ] Multi-user support
- [ ] Collaborative editing
- [ ] Template library
- [ ] Integration with external tools (Jira, GitHub)
- [ ] Analytics dashboard
- [ ] Mobile-responsive UI

---

## 🔗 Key Integration Points

### External Services
- **Anthropic Claude API**: AI/ML processing
- **Docker Hub**: Container images
- **GitHub**: Version control
- **npm (n8n)**: Workflow engine

### Internal Services
- **n8n ↔ BRD Parser**: HTTP (host.docker.internal:8000)
- **n8n ↔ Planning Agent**: Webhooks (localhost:5678)
- **Streamlit ↔ Master Orchestrator**: HTTP (localhost:5678)
- **n8n ↔ File System**: Volume mount (/data/projects)

### Future Integrations (TODO)
- **PostgreSQL**: Metadata storage
- **Redis**: Caching
- **Prometheus**: Monitoring
- **Grafana**: Dashboards
- **ELK Stack**: Logging
- **Jira**: Project management
- **GitHub**: Code repositories
- **Slack**: Notifications

---

## 📝 Notes

- **Token usage** is the primary cost driver (Anthropic API)
- **Rate limiting** is the main bottleneck for testing
- **File-based storage** works for MVP but needs migration to DB for production
- **Single AI model** (Claude Haiku) keeps costs low but limits quality
- **No authentication** means this is currently for personal/internal use only

---

**Legend:**
- ✅ **Implemented & Working**
- ⏸️ **TODO / Not Started**
- 🔮 **Future Enhancement**

---

*Last Updated: November 23, 2025*

