# 🚀 End-to-End Setup Guide
## BRD to Engineering Artifacts Pipeline

This guide walks you through setting up and testing the complete pipeline:
**PDF BRD → Parser → Engineering Plan → Project Schedule**

---

## 📋 Prerequisites

### Required Software
- **Docker & Docker Compose** - For running services
- **jq** - JSON processor (`brew install jq`)
- **curl** - API testing
- **Anthropic API Key** - For AI processing

### System Requirements
- macOS/Linux
- 8GB RAM minimum
- 10GB free disk space

---

## 🏗️ Architecture Overview

```
┌─────────┐     ┌──────────┐     ┌─────────────┐     ┌──────────┐
│  PDF    │────▶│   BRD    │────▶│ Engineering │────▶│ Project  │
│  BRD    │     │  Parser  │     │    Plan     │     │ Schedule │
└─────────┘     └──────────┘     └─────────────┘     └──────────┘
                     ▲                   ▲                  ▲
                     │                   │                  │
              FastAPI Service      n8n Workflow      n8n Workflow
              (Port 8000)         (Planning Agent)  (Planning Agent)
                                        
                     └───────────────────┴──────────────────┘
                                Master Orchestrator
                                  (n8n Workflow)
```

---

## ⚙️ Setup Steps

### Step 1: Configure Environment

Create `.env` file in `brd_parser/` directory:

```bash
cd /Users/udayammanagi/Udays-Folder/IK/brd_agent_em

# Create .env file
cat > brd_parser/.env << 'EOF'
ANTHROPIC_API_KEY=your_api_key_here
EOF

# Replace with your actual API key
nano brd_parser/.env
```

Get your Anthropic API key from: https://console.anthropic.com/

### Step 2: Start All Services

```bash
cd /Users/udayammanagi/Udays-Folder/IK/brd_agent_em

# Start n8n + BRD Parser
docker-compose up -d

# Verify services are running
docker-compose ps

# Check logs
docker-compose logs -f
```

**Expected Output:**
```
NAME                  STATUS    PORTS
n8n-brd-agent         Up        0.0.0.0:5678->5678/tcp
brd-parser-service    Up        0.0.0.0:8000->8000/tcp
```

### Step 3: Verify Services

```bash
# Check n8n
curl http://localhost:5678

# Check BRD Parser
curl http://localhost:8000/health

# Expected: {"status":"healthy","anthropic_configured":true}
```

### Step 4: Import n8n Workflows

1. **Open n8n**: http://localhost:5678
2. **Login**: admin / change-this-password (or your configured credentials)

3. **Import workflows** (in order):

   **a) BRD Input Cleaner:**
   - Click "+ Add workflow"
   - Click "..." → "Import from File"
   - Select: `brd_parser/brd_input_cleaner.json`
   - Click "Save"
   - Toggle "Activate" (top right)

   **b) Engineering Plan Generator:**
   - Click "+ Add workflow"
   - Click "..." → "Import from File"
   - Select: `n8n_flows/planning_agent/engineering_plan/structured_plan_generator.json`
   - Click "Save"
   - Toggle "Activate"

   **c) Project Schedule Generator:**
   - Click "+ Add workflow"
   - Click "..." → "Import from File"
   - Select: `n8n_flows/planning_agent/project_schedule/project_schedule_generator.json`
   - Click "Save"
   - Toggle "Activate"

   **d) Master Orchestrator:**
   - Click "+ Add workflow"
   - Click "..." → "Import from File"
   - Select: `n8n_flows/master_orchestrator.json`
   - Click "Save"
   - Toggle "Activate"

4. **Verify Anthropic credentials** are configured in n8n:
   - Go to Settings → Credentials
   - Find "Anthropic API" (Header Auth)
   - Verify API key is set

---

## 🧪 Testing

### Option 1: Automated End-to-End Test ✅ RECOMMENDED

```bash
cd /Users/udayammanagi/Udays-Folder/IK/brd_agent_em

# Run the automated test
tests/integration/test_e2e_orchestrator.sh

# Or with a specific JSON BRD file
tests/integration/test_e2e_orchestrator.sh sample_inputs/brds/brd_input_cleaner.json
```

**Expected Output:**
```
🚀 End-to-End Orchestrator Test
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ jq installed
✓ Docker is running
✓ n8n is accessible
✓ BRD Parser is accessible

🔄 Starting End-to-End Test...

✓ Orchestration completed successfully! (HTTP 200)

📊 Results:
  orchestration_id: orch_1700000000000
  status: success
  project_name: E-Commerce Platform
  features_count: 3
  duration: 45 seconds

✅ END-TO-END TEST PASSED!
```

### Option 2: Manual Testing

#### Test 1: BRD Parser Only

```bash
# Test with sample text
curl -X POST http://localhost:8000/parse/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Project: Customer Portal. Features: User login, Dashboard, Profile management..."}' \
  | jq '.'
```

#### Test 2: Engineering Plan Only

```bash
curl -X POST http://localhost:5678/webhook-test/planning-agent/engineering-plan \
  -H "Content-Type: application/json" \
  -d @sample_inputs/brds/brd_input_cleaner.json \
  | jq '.'
```

#### Test 3: Complete Pipeline (Orchestrator)

```bash
# Using JSON BRD
curl -X POST http://localhost:5678/webhook-test/orchestrator/process-brd \
  -H "Content-Type: application/json" \
  -d '{
    "brd_data": {
      "project": {
        "name": "Test Project",
        "description": "Test description",
        "objectives": ["Objective 1"],
        "constraints": ["Constraint 1"]
      },
      "features": [
        {
          "id": "F001",
          "name": "Feature 1",
          "description": "Description",
          "priority": "High",
          "requirements": ["Requirement 1"]
        }
      ],
      "stakeholders": ["Team 1"],
      "technical_requirements": {
        "platforms": ["Web"],
        "integrations": ["API"],
        "performance": "Fast",
        "security": "High",
        "scalability": "Medium"
      },
      "success_criteria": ["Criteria 1"]
    }
  }' \
  | jq '.'
```

---

## 📁 Output Files

Generated files are saved to:

```
sample_inputs/outputs/
├── engineering_plans/
│   └── engineering_plan_<project>_v<version>_<timestamp>.json
└── project_schedules/
    └── project_schedule_<project>_v<version>_<timestamp>.json
```

View latest outputs:
```bash
# Engineering Plans
ls -lht sample_inputs/outputs/engineering_plans/ | head -5

# Project Schedules
ls -lht sample_inputs/outputs/project_schedules/ | head -5

# View specific file
cat $(ls -t sample_inputs/outputs/engineering_plans/*.json | head -1) | jq '.'
```

---

## 🔧 Troubleshooting

### Issue: BRD Parser service won't start

```bash
# Check logs
docker-compose logs brd-parser

# Common fixes:
# 1. Missing ANTHROPIC_API_KEY
echo "ANTHROPIC_API_KEY=your_key" > brd_parser/.env

# 2. Port 8000 in use
lsof -ti:8000 | xargs kill -9
docker-compose restart brd-parser

# 3. Rebuild image
docker-compose build brd-parser
docker-compose up -d brd-parser
```

### Issue: n8n workflows return 404

**Problem**: Using `/webhook/` instead of `/webhook-test/`

**Fix**: For testing, always use `/webhook-test/` URLs:
- ✅ `http://localhost:5678/webhook-test/orchestrator/process-brd`
- ❌ `http://localhost:5678/webhook/orchestrator/process-brd`

### Issue: "Anthropic API error"

```bash
# 1. Verify API key in BRD Parser
curl http://localhost:8000/health

# Should return: "anthropic_configured": true

# 2. Check n8n credentials
# Go to n8n UI → Settings → Credentials → Anthropic API
# Verify x-api-key is set

# 3. Test API key directly
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-3-haiku-20240307","max_tokens":100,"messages":[{"role":"user","content":"Hi"}]}'
```

### Issue: Workflows time out

```bash
# Increase timeouts in n8n
# Edit docker-compose.yml:
environment:
  - EXECUTIONS_TIMEOUT=3600
  - EXECUTIONS_TIMEOUT_MAX=7200

# Restart
docker-compose restart n8n
```

### Issue: Files not being saved

```bash
# Check volume mount
docker-compose config | grep volumes

# Should include:
# - /Users/udayammanagi/Udays-Folder:/data/projects

# Check permissions
ls -la sample_inputs/outputs/

# Create directories if missing
mkdir -p sample_inputs/outputs/{engineering_plans,project_schedules}
```

---

## 📊 Monitoring

### View Real-time Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f brd-parser
docker-compose logs -f n8n

# Last 100 lines
docker-compose logs --tail=100 brd-parser
```

### Check Service Health

```bash
# BRD Parser
watch -n 2 'curl -s http://localhost:8000/health | jq'

# n8n
curl http://localhost:5678/healthz
```

### Monitor n8n Executions

1. Open n8n: http://localhost:5678
2. Click "Executions" (left sidebar)
3. See all workflow runs with status and duration

---

## 🎯 Success Checklist

- [ ] Docker services running (n8n + BRD Parser)
- [ ] BRD Parser health check passes
- [ ] All 4 n8n workflows imported and activated
- [ ] Anthropic credentials configured
- [ ] Automated test passes
- [ ] Output files generated correctly

---

## 🚀 Next Steps

### 1. Add More BRD Samples
```bash
# Add sample BRDs to test with
cp your_brd.pdf sample_inputs/brds/
```

### 2. Test with PDF BRDs
```bash
# Upload PDF to parser
curl -X POST http://localhost:8000/parse/pdf \
  -F "file=@sample_inputs/brds/your_brd.pdf" \
  | jq '.'
```

### 3. Build Streamlit UI
- See `IMPLEMENTATION_PLAN.md` Phase 3
- Create user-friendly web interface
- Add progress tracking

### 4. Add Design Agent Workflows
- Architecture Generator
- PoC Document Generator
- Tech Stack Recommendations

---

## 📚 Additional Documentation

- **BRD Parser**: `brd_parser/README.md`
- **Planning Agent**: `n8n_flows/planning_agent/WORKFLOW_GUIDE.md`
- **Docker Setup**: `DOCKER_SETUP.md`
- **Implementation Plan**: `IMPLEMENTATION_PLAN.md`
- **Integration Tests**: `tests/integration/README.md`

---

## 🆘 Need Help?

1. Check service logs: `docker-compose logs -f`
2. Verify n8n workflow executions in UI
3. Review error messages in test output
4. Check this guide's troubleshooting section

---

**Ready to test? Run:**

```bash
tests/integration/test_e2e_orchestrator.sh
```

🎉 **Your end-to-end BRD processing pipeline is now ready!**

