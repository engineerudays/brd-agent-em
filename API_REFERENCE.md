# 🔌 BRD Agent - API Reference & Architecture

**Technical Documentation for Developers**

Version: 1.0  
Last Updated: November 22, 2025

---

## 📋 Table of Contents

1. [System Architecture](#system-architecture)
2. [API Endpoints](#api-endpoints)
3. [Data Schemas](#data-schemas)
4. [Workflow Integration](#workflow-integration)
5. [Error Handling](#error-handling)
6. [Performance & Scalability](#performance--scalability)
7. [Security](#security)
8. [Extension Guide](#extension-guide)

---

## 🏗️ System Architecture

### Overview

The BRD Agent uses a **multi-agent architecture** orchestrated by n8n workflows with a Streamlit frontend.

```
┌─────────────────┐
│  Streamlit UI   │ (Port 8501)
│  (Frontend)     │
└────────┬────────┘
         │ HTTP POST
         ↓
┌─────────────────┐
│   n8n Master    │ (Port 5678)
│  Orchestrator   │
└────────┬────────┘
         │
    ┌────┴────┬─────────┬────────────┐
    ↓         ↓         ↓            ↓
┌────────┐┌────────┐┌────────┐┌──────────┐
│  BRD   ││Engineer││Project ││  Design  │
│ Parser ││  Plan  ││Schedule││  Agent   │
└────────┘└────────┘└────────┘└──────────┘
    │         │         │            │
    └─────────┴─────────┴────────────┘
                  │
            ┌─────┴─────┐
            │ Anthropic │
            │  Claude   │
            └───────────┘
```

### Components

| Component | Technology | Port | Purpose |
|-----------|-----------|------|---------|
| Frontend UI | Streamlit (Python) | 8501 | User interface |
| Master Orchestrator | n8n Workflow | 5678 | Pipeline coordination |
| BRD Parser | FastAPI (Python) | 8000 | PDF/text extraction |
| Engineering Plan Agent | n8n Workflow | 5678 | Plan generation |
| Project Schedule Agent | n8n Workflow | 5678 | Timeline creation |
| AI Engine | Anthropic Claude | External | Content generation |

### Data Flow

1. **Input**: User uploads BRD (PDF/JSON) via Streamlit UI
2. **Orchestration**: Master Orchestrator receives request
3. **Parsing** (if PDF): BRD Parser extracts structured data
4. **Engineering Plan**: Claude generates implementation plan
5. **Project Schedule**: Claude creates timeline with phases
6. **Response**: Artifacts returned to UI and saved to disk
7. **Display**: UI renders human-readable results + Gantt chart

---

## 🔗 API Endpoints

### 1. Master Orchestrator

**Endpoint**: `/webhook/orchestrator/process-brd-v2`

**Method**: `POST`

**Description**: Main entry point for BRD processing. Orchestrates the entire pipeline.

**Request**:
```json
{
  "project": {
    "name": "Project Name",
    "description": "Description"
  },
  "features": [...],
  "technical_requirements": {...}
}
```

Or for PDF:
```json
{
  "pdf_file": "base64_encoded_pdf_content",
  "filename": "document.pdf"
}
```

**Response**:
```json
{
  "status": "success",
  "message": "BRD processed successfully through entire pipeline",
  "stages_completed": [
    "brd_parsing",
    "engineering_plan",
    "project_schedule"
  ],
  "timestamp": "2025-11-22T10:43:39.878Z",
  "note": "Generated files saved to sample_inputs/outputs/",
  "engineering_plan": {
    "project_overview": {...},
    "feature_breakdown": [...],
    "technical_architecture": {...},
    "implementation_phases": [...],
    "risk_analysis": [...],
    "resource_requirements": {...},
    "success_metrics": [...]
  },
  "project_schedule": {
    "project_info": {...},
    "phases": [...],
    "resource_allocation": [...],
    "critical_path": {...},
    "assumptions": [...],
    "constraints": [...]
  }
}
```

**Error Response**:
```json
{
  "status": "error",
  "message": "Error description",
  "timestamp": "2025-11-22T10:43:39.878Z"
}
```

**Status Codes**:
- `200`: Success
- `400`: Invalid request (bad BRD format)
- `500`: Server error (workflow failure)
- `504`: Timeout

---

### 2. BRD Parser

**Endpoint**: `/webhook/brd-parser/upload`

**Method**: `POST`

**Description**: Extracts structured data from PDF or raw text BRDs.

**Request**:
```json
{
  "body": {
    "pdf_file": "base64_encoded_content",
    "filename": "brd.pdf"
  }
}
```

Or:
```json
{
  "body": {
    "raw_brd_text": "Plain text BRD content..."
  }
}
```

**Response**:
```json
{
  "status": "success",
  "parsed_brd": {
    "document_info": {...},
    "executive_summary": "...",
    "business_objectives": [...],
    "project_scope": {...},
    "stakeholders": [...],
    "requirements": {
      "functional": [...],
      "non_functional": [...]
    },
    "constraints_assumptions_dependencies": {...}
  },
  "metadata": {
    "parsing_method": "pdf" | "text",
    "timestamp": "2025-11-22T10:43:39.878Z"
  }
}
```

**Anthropic API**: Used internally for intelligent extraction

---

### 3. Engineering Plan Generator

**Endpoint**: `/webhook/planning-agent/engineering-plan`

**Method**: `POST`

**Description**: Generates detailed engineering implementation plan.

**Request**:
```json
{
  "raw_brd_text": "{...json_stringified_brd...}"
}
```

**Response**:
```json
{
  "engineering_plan": {
    "project_overview": {
      "name": "string",
      "description": "string",
      "objectives": ["string"]
    },
    "feature_breakdown": [
      {
        "feature_id": "F001",
        "feature_name": "string",
        "description": "string",
        "priority": "Critical|High|Medium|Low",
        "complexity": "High|Medium|Low",
        "estimated_effort": "string",
        "dependencies": ["string"],
        "technical_requirements": ["string"],
        "acceptance_criteria": ["string"]
      }
    ],
    "technical_architecture": {
      "system_components": ["string"],
      "integration_points": ["string"],
      "data_flow": "string",
      "security_considerations": ["string"]
    },
    "implementation_phases": [
      {
        "phase_number": 1,
        "phase_name": "string",
        "description": "string",
        "features_included": ["string"],
        "estimated_duration": "string",
        "deliverables": ["string"]
      }
    ],
    "risk_analysis": [
      {
        "risk_id": "R001",
        "description": "string",
        "impact": "High|Medium|Low",
        "probability": "High|Medium|Low",
        "mitigation_strategy": "string"
      }
    ],
    "resource_requirements": {
      "team_composition": ["string"],
      "tools_and_technologies": ["string"],
      "infrastructure_needs": ["string"]
    },
    "success_metrics": [
      {
        "metric_name": "string",
        "target_value": "string",
        "measurement_method": "string"
      }
    ]
  },
  "metadata": {
    "generated_at": "2025-11-22T10:43:39.878Z",
    "model": "claude-3-haiku-20240307"
  },
  "filename": "engineering_plan_project_name_v1_timestamp.json"
}
```

---

### 4. Project Schedule Generator

**Endpoint**: `/webhook/planning-agent/project-schedule`

**Method**: `POST`

**Description**: Creates project timeline based on engineering plan.

**Request**:
```json
{
  "engineering_plan": {
    "project_overview": {...},
    "feature_breakdown": [...],
    "implementation_phases": [...]
  }
}
```

**Response**:
```json
{
  "project_schedule": {
    "project_info": {
      "start_date": "2025-01-01",
      "end_date": "2025-06-30",
      "total_duration_weeks": 26
    },
    "phases": [
      {
        "phase_id": "P1",
        "phase_name": "MVP Release",
        "start_date": "2025-01-01",
        "end_date": "2025-03-31",
        "duration_weeks": 13,
        "milestones": [
          {
            "name": "Requirements Complete",
            "target_date": "2025-01-15",
            "description": "string"
          }
        ],
        "tasks": [
          {
            "task_id": "T001",
            "task_name": "string",
            "start_date": "2025-01-01",
            "end_date": "2025-01-15",
            "assigned_to": "string",
            "dependencies": ["string"]
          }
        ]
      }
    ],
    "resource_allocation": [...],
    "critical_path": {
      "total_duration": "26 weeks",
      "critical_tasks": ["string"]
    },
    "key_deliverables": [...],
    "risk_timeline": {...},
    "assumptions": ["string"],
    "constraints": ["string"]
  },
  "metadata": {
    "generated_at": "2025-11-22T10:43:39.878Z",
    "model": "claude-3-haiku-20240307"
  }
}
```

---

## 📦 Data Schemas

### BRD Input Schema

```typescript
interface BRD {
  // Option 1: PDF Upload
  pdf_file?: string;  // base64 encoded
  filename?: string;
  
  // Option 2: Structured JSON
  project?: {
    name: string;
    description: string;
    objectives?: string[];
    constraints?: string[];
  };
  
  features?: Feature[];
  stakeholders?: Stakeholder[];
  technical_requirements?: TechnicalRequirements;
  success_criteria?: string[];
  
  // Option 3: Raw Text
  raw_brd_text?: string;  // JSON stringified
}

interface Feature {
  id: string;
  name: string;
  description: string;
  priority: "High" | "Medium" | "Low";
  requirements: string[];
}
```

### Engineering Plan Schema

```typescript
interface EngineeringPlan {
  project_overview: {
    name: string;
    description: string;
    objectives: string[];
  };
  
  feature_breakdown: FeatureDetail[];
  technical_architecture: Architecture;
  implementation_phases: Phase[];
  risk_analysis: Risk[];
  resource_requirements: Resources;
  success_metrics: Metric[];
}

interface FeatureDetail {
  feature_id: string;
  feature_name: string;
  description: string;
  priority: "Critical" | "High" | "Medium" | "Low";
  complexity: "High" | "Medium" | "Low";
  estimated_effort: string;
  dependencies: string[];
  technical_requirements: string[];
  acceptance_criteria: string[];
}
```

### Project Schedule Schema

```typescript
interface ProjectSchedule {
  project_info: {
    start_date: string;  // YYYY-MM-DD
    end_date: string;
    total_duration_weeks: number;
  };
  
  phases: SchedulePhase[];
  resource_allocation: ResourceAllocation[];
  critical_path: CriticalPath;
  key_deliverables: Deliverable[];
  risk_timeline: RiskTimeline;
  assumptions: string[];
  constraints: string[];
}

interface SchedulePhase {
  phase_id: string;
  phase_name: string;
  start_date: string;
  end_date: string;
  duration_weeks: number;
  milestones: Milestone[];
  tasks: Task[];
}
```

---

## 🔄 Workflow Integration

### n8n Workflow Structure

#### Master Orchestrator
```javascript
// Webhook → Initialize → Check Format → Parser/Direct → 
// Engineering Plan → Schedule → Response
```

**Key Nodes**:
1. **Webhook - Process BRD**: Entry point
2. **Initialize Orchestration**: Extract/validate input
3. **Check Needs Parsing**: PDF detection
4. **Call BRD Parser**: PDF processing (conditional)
5. **Normalize BRD Format**: Ensure consistent structure
6. **Generate Engineering Plan**: HTTP Request to plan agent
7. **Update After Plan**: Extract plan data
8. **Generate Project Schedule**: HTTP Request to schedule agent
9. **Prepare Success Response**: Combine results
10. **Respond Success**: Return to client

#### Engineering Plan Workflow
```javascript
// Webhook → Validate → Parse BRD → Prepare Prompt → 
// Call Claude API → Parse Response → Save File → Response
```

#### Project Schedule Workflow
```javascript
// Webhook → Parse Plan → Prepare Prompt → 
// Call Claude API → Parse Response → Save File → Response
```

### Adding Custom Workflows

To add a new agent:

1. **Create n8n Workflow**:
   - Webhook trigger
   - Input validation
   - Processing logic
   - Response formatting

2. **Update Master Orchestrator**:
   - Add HTTP Request node
   - Connect to workflow sequence
   - Update response preparation

3. **Update UI** (optional):
   - Add display function in `utils.py`
   - Update Results tab in `app.py`

**Example**:
```javascript
// In Master Orchestrator, add after "Generate Project Schedule":
{
  "node": "Generate Design Artifacts",
  "type": "httpRequest",
  "url": "http://localhost:5678/webhook/design-agent/architecture",
  "method": "POST",
  "body": "={{ $json }}"
}
```

---

## ⚠️ Error Handling

### Error Types

| Error Type | Code | Retry? | Description |
|------------|------|--------|-------------|
| Validation Error | 400 | No | Invalid BRD format |
| Timeout | 504 | Yes | Request exceeded timeout |
| Connection Error | 0 | Yes | Network issue |
| Server Error | 500+ | Yes | Backend failure |
| Rate Limit | 429 | Yes | Too many requests |
| JSON Parse Error | 400 | No | Invalid JSON response |

### Retry Strategy

**Exponential Backoff**:
```python
attempt = 0
wait_time = 0

while attempt < max_retries:
    try:
        response = make_request()
        return response
    except RetryableError:
        attempt += 1
        wait_time = (2 ** attempt) * 2  # 2s, 4s, 8s
        sleep(wait_time)
```

**Retry Logic**:
- Max attempts: 3
- Wait times: 2s, 4s, 8s
- Total max wait: 14 seconds
- Retryable: Timeout, Connection, 5xx errors
- Non-retryable: 4xx errors, JSON errors

---

## 📈 Performance & Scalability

### Performance Metrics

| Operation | Time | Bottleneck |
|-----------|------|------------|
| PDF Upload | 0.5-2s | Network, file size |
| PDF Parsing | 5-15s | Claude API, PDF complexity |
| Engineering Plan | 20-40s | Claude API tokens |
| Project Schedule | 15-30s | Claude API tokens |
| Total (PDF) | 60-90s | Sequential processing |
| Total (JSON) | 35-70s | Sequential processing |

### Optimization Strategies

1. **Parallel Processing** (Future):
   ```
   BRD Parser
       ↓
   ┌───────┬────────┐
   │ Plan  │ Design │ (Parallel)
   └───┬───┴────┬───┘
       ↓        ↓
   Schedule  Architecture
   ```

2. **Caching**:
   - Cache parsed BRDs (Redis)
   - Cache AI responses for identical inputs
   - Session-based caching in UI

3. **Batch Processing**:
   - Queue multiple BRDs
   - Process in background
   - Notify on completion

### Scaling

**Horizontal Scaling**:
```yaml
version: '3.8'
services:
  n8n:
    replicas: 3
    deploy:
      mode: replicated
  
  brd-parser:
    replicas: 2
    deploy:
      mode: replicated
  
  streamlit:
    replicas: 2
    deploy:
      mode: replicated
```

**Load Balancing**:
- Use nginx or HAProxy
- Session affinity for Streamlit
- Round-robin for stateless APIs

---

## 🔒 Security

### Authentication

Currently: **No authentication** (local development)

**Production Recommendations**:

1. **n8n Workflows**:
   ```javascript
   // Add API key validation
   const apiKey = $input.item.json.headers['x-api-key'];
   if (apiKey !== process.env.API_KEY) {
     throw new Error('Unauthorized');
   }
   ```

2. **Streamlit UI**:
   ```python
   # Add login page
   if 'authenticated' not in st.session_state:
       username = st.text_input("Username")
       password = st.text_input("Password", type="password")
       if st.button("Login"):
           if authenticate(username, password):
               st.session_state['authenticated'] = True
   ```

### Data Security

**Sensitive Data**:
- BRD documents (may contain confidential info)
- Generated artifacts (IP protection)

**Best Practices**:
1. **Encryption at Rest**: Encrypt output files
2. **Encryption in Transit**: HTTPS only
3. **Access Control**: Role-based permissions
4. **Audit Logging**: Track who accesses what
5. **Data Retention**: Auto-delete old artifacts

### API Keys

**Required Keys**:
```bash
# .env file
ANTHROPIC_API_KEY=sk-ant-xxx  # Claude AI
N8N_ENCRYPTION_KEY=xxx         # n8n credentials
```

**Key Rotation**:
- Rotate quarterly
- Use secrets manager (AWS Secrets Manager, HashiCorp Vault)
- Never commit to git

---

## 🔧 Extension Guide

### Adding a New Agent

#### Step 1: Create Workflow

```javascript
// new_agent.json
{
  "name": "New Agent - Feature X",
  "nodes": [
    {
      "name": "Webhook - Receive Input",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "new-agent/feature-x",
        "httpMethod": "POST"
      }
    },
    // ... processing nodes ...
    {
      "name": "Respond with Results",
      "type": "n8n-nodes-base.respondToWebhook"
    }
  ]
}
```

#### Step 2: Integrate with Orchestrator

```javascript
// In master_orchestrator.json, add node:
{
  "name": "Call New Agent",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "method": "POST",
    "url": "http://localhost:5678/webhook/new-agent/feature-x",
    "jsonBody": "={{ $json }}"
  }
}
```

#### Step 3: Update UI

```python
# In frontend/utils.py
def display_feature_x(data: Dict[str, Any]) -> None:
    """Display Feature X results"""
    import streamlit as st
    
    if not data:
        st.warning("No Feature X data available.")
        return
    
    with st.expander("🎯 Feature X Results"):
        st.json(data)

# In frontend/app.py, add to render_results_tab():
if result.get('feature_x'):
    st.header("🎯 Feature X")
    utils.display_feature_x(result['feature_x'])
```

### Custom AI Prompts

Modify prompts in workflow Code nodes:

```javascript
// In "Prepare AI Prompt" node
const customPrompt = `
You are an expert in ${domain}.
Given this BRD: ${brdData}
Generate: ${outputType}
Format: ${format}
Constraints: ${constraints}
`;

return {
  json: {
    prompt: customPrompt
  }
};
```

---

## 📚 API Client Examples

### Python

```python
import requests
import json

# Load BRD
with open('brd.json', 'r') as f:
    brd_data = json.load(f)

# Call orchestrator
response = requests.post(
    'http://localhost:5678/webhook/orchestrator/process-brd-v2',
    json=brd_data,
    headers={'Content-Type': 'application/json'},
    timeout=180
)

result = response.json()

# Save artifacts
with open('engineering_plan.json', 'w') as f:
    json.dump(result['engineering_plan'], f, indent=2)

with open('project_schedule.json', 'w') as f:
    json.dump(result['project_schedule'], f, indent=2)
```

### JavaScript/Node.js

```javascript
const axios = require('axios');
const fs = require('fs');

async function processBRD(brdData) {
  try {
    const response = await axios.post(
      'http://localhost:5678/webhook/orchestrator/process-brd-v2',
      brdData,
      {
        headers: { 'Content-Type': 'application/json' },
        timeout: 180000
      }
    );
    
    const result = response.data;
    
    // Save artifacts
    fs.writeFileSync(
      'engineering_plan.json',
      JSON.stringify(result.engineering_plan, null, 2)
    );
    
    return result;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
const brd = require('./brd.json');
processBRD(brd).then(result => {
  console.log('Success:', result.status);
});
```

### cURL

```bash
# JSON BRD
curl -X POST http://localhost:5678/webhook/orchestrator/process-brd-v2 \
  -H "Content-Type: application/json" \
  -d @brd.json \
  -o result.json

# PDF BRD (base64 encoded)
PDF_BASE64=$(base64 -i brd.pdf)
curl -X POST http://localhost:5678/webhook/orchestrator/process-brd-v2 \
  -H "Content-Type: application/json" \
  -d "{\"pdf_file\": \"$PDF_BASE64\", \"filename\": \"brd.pdf\"}" \
  -o result.json
```

---

## 📞 Support & Resources

### Technical Documentation
- **Main README**: `README.md`
- **Setup Guide**: `SETUP.md`
- **User Guide**: `USER_GUIDE.md`
- **This Document**: `API_REFERENCE.md`

### Code Locations
```
├── frontend/           # Streamlit UI
│   ├── app.py          # Main application
│   ├── utils.py        # Helper functions
│   └── config.py       # Configuration
├── n8n_flows/          # Workflow definitions
│   ├── master_orchestrator.json
│   └── planning_agent/
│       ├── engineering_plan/
│       └── project_schedule/
├── brd_parser/         # FastAPI service
│   ├── main.py
│   └── requirements.txt
└── tests/              # Integration tests
    └── integration/
```

### Getting Help
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: [Your contact]

---

**Last Updated**: November 22, 2025

*For the latest updates, check the GitHub repository.*

