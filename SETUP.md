# 🚀 Setup & Execution Guide
## BRD Agent - Multi-Agent System

Complete guide to set up and run the BRD to Engineering Artifacts pipeline.

---

## 📋 Prerequisites

### Required Software
- **Docker & Docker Compose** (v20.10+)
- **jq** - JSON processor
  ```bash
  # macOS
  brew install jq
  
  # Ubuntu/Debian
  sudo apt-get install jq
  ```
- **curl** - API testing (usually pre-installed)

### Required API Keys
- **Anthropic API Key** - Get from: https://console.anthropic.com/

### System Requirements
- **OS**: macOS or Linux
- **RAM**: 8GB minimum (16GB recommended)
- **Disk**: 10GB free space
- **Network**: Internet access for AI API calls

---

## 🏗️ Architecture Quick Reference

```
┌─────────┐     ┌──────────┐     ┌─────────────┐     ┌──────────┐
│  JSON   │────▶│   BRD    │────▶│ Engineering │────▶│ Project  │
│  BRD    │     │  Parser  │     │    Plan     │     │ Schedule │
└─────────┘     └──────────┘     └─────────────┘     └──────────┘
                     │                   │                  │
              FastAPI Service      n8n Workflow      n8n Workflow
              (Port 8000)         (Planning Agent)  (Planning Agent)
                                        
                     └───────────────────┴──────────────────┘
                                Master Orchestrator
                                  (n8n Workflow)
```

---

## ⚙️ Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/engineerudays/brd-agent-em.git
cd brd-agent-em
```

### Step 2: Configure Environment

Create `.env` file in `brd_parser/` directory:

```bash
# Create .env file
cat > brd_parser/.env << 'EOF'
ANTHROPIC_API_KEY=your_anthropic_api_key_here
EOF

# Edit with your actual API key
nano brd_parser/.env
```

**⚠️ Important:** Replace `your_anthropic_api_key_here` with your actual Anthropic API key.

### Step 3: Update Docker Compose Volumes

Edit `docker-compose.yml` and update the volume mount path to your local path:

```yaml
volumes:
  - /YOUR/LOCAL/PATH/brd_agent_em:/data/projects/IK/brd_agent_em
```

Replace `/YOUR/LOCAL/PATH/` with your actual directory path.

### Step 4: Start Services

```bash
# Start all services in detached mode
docker-compose up -d

# Verify services are running
docker-compose ps
```

**Expected Output:**
```
NAME                  STATUS    PORTS
n8n-brd-agent         Up        0.0.0.0:5678->5678/tcp
brd-parser-service    Up        0.0.0.0:8000->8000/tcp
```

### Step 5: Verify Health

```bash
# Check n8n (should return HTML)
curl http://localhost:5678

# Check BRD Parser
curl http://localhost:8000/health

# Expected: {"status":"healthy","anthropic_configured":true}
```

---

## 📦 n8n Workflow Setup

### Import Workflows

1. **Open n8n**: http://localhost:5678

2. **Import the following workflows in order:**

   a. **BRD Input Cleaner** (Required for parsing)
   - File: `brd_parser/brd_input_cleaner.json`
   - Import → Workflows → Import from File

   b. **Engineering Plan Generator**
   - File: `n8n_flows/planning_agent/engineering_plan/structured_plan_generator.json`

   c. **Project Schedule Generator**
   - File: `n8n_flows/planning_agent/project_schedule/project_schedule_generator.json`

   d. **Master Orchestrator**
   - File: `n8n_flows/master_orchestrator.json`

3. **Configure Anthropic Credentials** (for each workflow):
   - Go to: Settings → Credentials
   - Create new credential: "Anthropic Header Auth"
   - Header Name: `x-api-key`
   - Header Value: Your Anthropic API key

4. **Activate ALL workflows** (toggle switch should be blue/ON)

---

## 🧪 Testing

### Quick Test - End-to-End Pipeline

```bash
# Run the automated test script
./tests/integration/test_e2e_orchestrator.sh sample_inputs/brds/brd_input_cleaner.json
```

**Expected Output:**
```
🚀 End-to-End Orchestrator Test
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ jq installed
✓ n8n is reachable at http://localhost:5678
✓ BRD Parser is healthy at http://localhost:8000
✓ Test BRD file exists: sample_inputs/brds/brd_input_cleaner.json

📤 Sending BRD to orchestrator...
✓ Orchestrator request successful (HTTP 200)

📊 Results:
{
  "status": "success",
  "message": "BRD processed successfully through entire pipeline",
  "stages_completed": [
    "brd_parsing",
    "engineering_plan",
    "project_schedule"
  ],
  ...
}

✓ All stages completed:
  ✓ brd_parsing
  ✓ engineering_plan
  ✓ project_schedule

✓ END-TO-END TEST PASSED!
```

### Check Generated Outputs

```bash
# Engineering plans
ls -lh sample_inputs/outputs/engineering_plans/

# Project schedules
ls -lh sample_inputs/outputs/project_schedules/
```

---

## 🔄 Manual Testing

### Test Individual Workflows

#### 1. Test BRD Parser (Direct)

```bash
curl -X POST http://localhost:8000/api/parse \
  -H "Content-Type: application/json" \
  -d @sample_inputs/brds/brd_input_cleaner.json
```

#### 2. Test Engineering Plan Generator

```bash
# In n8n UI:
# 1. Open "Planning Agent - Engineering Plan Generator"
# 2. Click "Test workflow"
# 3. Send sample BRD data
```

#### 3. Test Full Orchestrator

```bash
curl -X POST http://localhost:5678/webhook/orchestrator/process-brd-v2 \
  -H "Content-Type: application/json" \
  -d @sample_inputs/brds/brd_input_cleaner.json
```

---

## 🐛 Troubleshooting

### Services Not Starting

```bash
# Check Docker logs
docker-compose logs

# For specific service
docker-compose logs brd-parser
docker-compose logs n8n
```

### BRD Parser "unhealthy"

```bash
# Check if API key is configured
cat brd_parser/.env

# Restart the service
docker-compose restart brd-parser

# Check logs
docker-compose logs -f brd-parser
```

### Workflows Not Activating

**Error:** "A webhook trigger uses a conflicting URL path"

**Solution:**
1. Delete all old/duplicate workflows in n8n
2. Re-import fresh workflows
3. Activate them one by one

### File Permission Issues

```bash
# Fix permissions for output directories
chmod -R 755 sample_inputs/outputs/
```

### Missing Output Files

**Check:**
1. Are all 4 workflows activated in n8n?
2. Check n8n execution logs for errors
3. Verify volume mount path in `docker-compose.yml`

---

## 🔧 Common Commands

### Docker Management

```bash
# Stop all services
docker-compose down

# Restart services
docker-compose restart

# View logs (follow mode)
docker-compose logs -f

# Rebuild after code changes
docker-compose up -d --build

# Clean everything and start fresh
docker-compose down -v
docker-compose up -d --build
```

### Check Service Status

```bash
# Quick health check
curl http://localhost:8000/health && echo " ✓ Parser OK"
curl -s http://localhost:5678 > /dev/null && echo " ✓ n8n OK"
```

---

## 📁 Project Structure

```
brd_agent_em/
├── brd_parser/              # FastAPI BRD Parser Service
│   ├── main.py             # Parser implementation
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env                # API keys (create this)
├── n8n_flows/              # n8n Workflow Definitions
│   ├── master_orchestrator.json
│   └── planning_agent/
│       ├── engineering_plan/
│       └── project_schedule/
├── sample_inputs/          # Test BRDs
│   ├── brds/              # Input BRD files
│   └── outputs/           # Generated artifacts (ignored by git)
├── tests/integration/      # Automated tests
│   └── test_e2e_orchestrator.sh
├── docker-compose.yml      # Service orchestration
└── README.md              # Project overview
```

---

## 🎯 Next Steps

After successful setup:

1. **Try with your own BRDs:**
   - Place JSON BRD files in `sample_inputs/brds/`
   - Run the test script with your file

2. **Explore n8n workflows:**
   - Modify prompts in AI nodes
   - Adjust output formats
   - Add custom validation

3. **Extend the system:**
   - Add Design Agent workflows
   - Implement Architecture workflows
   - Build Streamlit frontend

---

## 📚 Additional Resources

- **n8n Documentation**: https://docs.n8n.io/
- **Anthropic API**: https://docs.anthropic.com/
- **Docker Compose**: https://docs.docker.com/compose/

---

## 🆘 Getting Help

1. Check workflow execution logs in n8n UI
2. Review Docker logs: `docker-compose logs -f`
3. Verify API key configuration
4. Ensure all 4 workflows are activated
5. Check file permissions on output directories

---

**🎉 You're all set!** Run the test script and start processing BRDs.

