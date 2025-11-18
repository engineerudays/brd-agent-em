# Integration Tests

This directory contains integration tests for the BRD Multi-Agent System.

## 📁 Test Scripts

### 1. End-to-End Orchestrator Test ⭐ **RECOMMENDED**

**File**: `test_e2e_orchestrator.sh`

Tests the complete pipeline:
- PDF/JSON BRD → Parser → Engineering Plan → Project Schedule

**Features**:
- ✅ Comprehensive pre-flight checks
- ✅ Tests entire pipeline in one go
- ✅ Validates all stages
- ✅ Displays execution time and results
- ✅ Checks generated output files

**Usage** (from project root):
```bash
# Test with sample JSON data (built-in)
tests/integration/test_e2e_orchestrator.sh

# Test with your own JSON BRD
tests/integration/test_e2e_orchestrator.sh sample_inputs/brds/your_brd.json
```

**Requirements**:
- Docker running (n8n + BRD Parser)
- All workflows imported and activated
- `jq` installed (`brew install jq`)
- Anthropic API key configured

---

### 2. Project Schedule Generator Test

**File**: `test_schedule_generator.sh`

Tests the Project Schedule Generator workflow by:
- Taking an engineering plan as input
- Wrapping it in the correct format
- Sending it to the n8n workflow
- Verifying the response and output files

**Usage** (from project root):
```bash
# Test with latest engineering plan
tests/integration/test_schedule_generator.sh $(ls -t sample_inputs/outputs/engineering_plans/*.json | head -1)

# Test with specific file
tests/integration/test_schedule_generator.sh sample_inputs/outputs/engineering_plans/engineering_plan_example.json
```

**Requirements**:
- n8n running on http://localhost:5678
- Project Schedule Generator workflow imported and activated
- `jq` installed (`brew install jq`)

---

## 🎯 Running Tests

### Prerequisites

1. **n8n must be running**:
   ```bash
   docker-compose up -d
   ```

2. **Workflows must be imported and activated** in n8n UI

3. **jq must be installed**:
   ```bash
   brew install jq
   ```

### Test Workflow

1. **Generate Engineering Plan** (if you don't have one):
   ```bash
   curl -X POST http://localhost:5678/webhook/planning-agent/engineering-plan \
     -H "Content-Type: application/json" \
     -d @sample_inputs/brds/brd_input_cleaner.json
   ```

2. **Run Integration Test**:
   ```bash
   tests/integration/test_schedule_generator.sh $(ls -t sample_inputs/outputs/engineering_plans/*.json | head -1)
   ```

3. **Verify Output**:
   ```bash
   ls -lh sample_inputs/outputs/project_schedules/
   ```

---

## 📝 Adding New Integration Tests

When adding new integration tests:

1. **Create test script**: `test_{workflow_name}.sh`
2. **Make it executable**: `chmod +x test_{workflow_name}.sh`
3. **Follow naming convention**: `test_{agent}_{feature}.sh`
4. **Include usage help**: Display help when run without arguments
5. **Verify output**: Check for expected files/responses
6. **Document here**: Add section above

### Test Script Template

```bash
#!/bin/bash

# Test {Workflow Name}
# Usage: tests/integration/test_{workflow}.sh <input-file>

INPUT_FILE="$1"
N8N_URL="http://localhost:5678/webhook/{workflow-path}"

if [ -z "$INPUT_FILE" ]; then
  echo "Usage: tests/integration/test_{workflow}.sh <input-file>"
  exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
  echo "❌ Error: File not found: $INPUT_FILE"
  exit 1
fi

echo "🧪 Testing {Workflow Name}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📄 Input: $(basename $INPUT_FILE)"
echo "🔗 Endpoint: $N8N_URL"
echo ""

# Process and send request
echo "⏳ Sending request..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$N8N_URL" \
  -H "Content-Type: application/json" \
  -d @"$INPUT_FILE")

# Extract HTTP status code
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ]; then
  echo "✅ Success! (HTTP $HTTP_CODE)"
  echo "$RESPONSE_BODY" | jq '.'
else
  echo "❌ Error! (HTTP $HTTP_CODE)"
  echo "$RESPONSE_BODY"
fi
```

---

## 🔍 Troubleshooting

### Common Issues

**Error: "Workflow not found" (404)**
- Check if workflow is imported in n8n
- Verify webhook path matches the workflow configuration
- Ensure workflow is activated (toggle is ON/blue)

**Error: "jq: command not found"**
```bash
brew install jq
```

**Error: "Connection refused"**
- Make sure n8n is running: `docker ps`
- Start n8n: `docker-compose up -d`
- Check port: `lsof -i :5678`

**Error: "ENOENT: no such file or directory"**
- Verify Docker volume mounting in `docker-compose.yml`
- Restart n8n: `docker-compose restart`
- Check absolute paths in workflow configurations

---

## 📊 Test Coverage

### Completed ✅
- [ ] Planning Agent - Engineering Plan Generator (manual testing)
- [x] Planning Agent - Project Schedule Generator (automated script)

### Planned ⏳
- [ ] Design Agent - Architecture Generator
- [ ] Design Agent - PoC Document Generator
- [ ] Design Agent - Tech Stack Recommendations
- [ ] BRD Parser Agent
- [ ] Master Orchestrator (end-to-end)

---

## 🎯 Future Enhancements

- [ ] Add automated test suite runner (`run_all_tests.sh`)
- [ ] Add test data fixtures
- [ ] Add result validation (schema checks)
- [ ] Add performance benchmarks
- [ ] Add CI/CD integration (GitHub Actions)
- [ ] Add test reporting (HTML/JSON output)

---

For detailed testing instructions, see:
- `n8n_flows/planning_agent/PROJECT_SCHEDULE_TESTING.md`
- `n8n_flows/planning_agent/TEST_REQUESTS.md`

