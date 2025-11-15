# 🗓️ Project Schedule Generator - Testing Guide

## 📋 Overview

The **Project Schedule Generator** takes an Engineering Plan as input and generates a detailed project schedule with:
- Phase timelines and milestones
- Task breakdowns with dependencies
- Resource allocation
- Critical path analysis
- Risk timeline with contingency buffers

---

## 🚀 Setup Steps

### Step 1: Import the Workflow into n8n

1. Open n8n: http://localhost:5678
2. Click **"+ Add workflow"** (or open existing if already imported)
3. Click the **three dots** (⋮) in top right → **Import from File**
4. Select: `/Users/udayammanagi/Udays-Folder/IK/brd_agent_em/n8n_flows/planning_agent/project_schedule/project_schedule_generator.json`
5. Click **"Save"** (top right)
6. Click **"Activate"** toggle (top right) to enable the webhook

### Step 2: Verify Webhook URL

The webhook should be available at:
```
POST http://localhost:5678/webhook/planning-agent/project-schedule
```

---

## 🧪 Testing Options

### Option 1: Use Previously Generated Engineering Plan ✅ RECOMMENDED

You already have engineering plans generated! Use one of them:

```bash
cd /Users/udayammanagi/Udays-Folder/IK/brd_agent_em

# Use your existing engineering plan
curl -X POST http://localhost:5678/webhook/planning-agent/project-schedule \
  -H "Content-Type: application/json" \
  -d @sample_inputs/outputs/engineering_plans/engineering_plan_customer_onboarding_and_success_portal_cosp_brd_v1_2025-11-15T15-07-55.json
```

**Wait!** The file format needs to be wrapped. Let me create a test script for you...

### Option 2: Two-Step Process (Generate → Schedule)

**Step 1**: Generate Engineering Plan
```bash
cd /Users/udayammanagi/Udays-Folder/IK/brd_agent_em

curl -X POST http://localhost:5678/webhook/planning-agent/engineering-plan \
  -H "Content-Type: application/json" \
  -d @sample_inputs/brds/brd_input_cleaner.json \
  -o /tmp/eng_plan.json
```

**Step 2**: Generate Schedule from Plan
```bash
# Wrap the engineering plan in the expected format
jq '{engineering_plan: .}' /tmp/eng_plan.json | \
curl -X POST http://localhost:5678/webhook/planning-agent/project-schedule \
  -H "Content-Type: application/json" \
  -d @-
```

---

## 📝 Test Script (Easiest Way)

We have a simple test script that handles the format conversion:

**File**: `tests/integration/test_schedule_generator.sh`

```bash
#!/bin/bash

# Test Project Schedule Generator

ENGINEERING_PLAN_FILE="$1"
N8N_URL="http://localhost:5678/webhook/planning-agent/project-schedule"

if [ -z "$ENGINEERING_PLAN_FILE" ]; then
  echo "Usage: tests/integration/test_schedule_generator.sh <path-to-engineering-plan.json>"
  echo ""
  echo "Example:"
  echo "  tests/integration/test_schedule_generator.sh sample_inputs/outputs/engineering_plans/engineering_plan_customer_onboarding_and_success_portal_cosp_brd_v1_2025-11-15T15-07-55.json"
  exit 1
fi

if [ ! -f "$ENGINEERING_PLAN_FILE" ]; then
  echo "Error: File not found: $ENGINEERING_PLAN_FILE"
  exit 1
fi

echo "🧪 Testing Project Schedule Generator"
echo "📄 Input: $ENGINEERING_PLAN_FILE"
echo "🔗 Endpoint: $N8N_URL"
echo ""

# Wrap the engineering plan in the expected format
WRAPPED_PAYLOAD=$(jq '{engineering_plan: .}' "$ENGINEERING_PLAN_FILE")

# Send request
echo "⏳ Sending request..."
RESPONSE=$(echo "$WRAPPED_PAYLOAD" | curl -s -X POST "$N8N_URL" \
  -H "Content-Type: application/json" \
  -d @-)

echo "✅ Response received:"
echo "$RESPONSE" | jq '.'

echo ""
echo "📁 Check output at: sample_inputs/outputs/project_schedules/"
ls -lh sample_inputs/outputs/project_schedules/ 2>/dev/null | tail -5
```

---

## 🎯 Quick Test Commands

### Option A: Use Test Script (Recommended) ✅

```bash
cd /Users/udayammanagi/Udays-Folder/IK/brd_agent_em

# Test with latest engineering plan
tests/integration/test_schedule_generator.sh $(ls -t sample_inputs/outputs/engineering_plans/*.json | head -1)

# Or test with specific file
tests/integration/test_schedule_generator.sh sample_inputs/outputs/engineering_plans/engineering_plan_customer_onboarding_and_success_portal_cosp_brd_v1_2025-11-15T15-07-55.json
```

### Option B: Manual cURL Test

```bash
cd /Users/udayammanagi/Udays-Folder/IK/brd_agent_em

# Find the latest engineering plan
LATEST_PLAN=$(ls -t sample_inputs/outputs/engineering_plans/*.json | head -1)
echo "Using plan: $LATEST_PLAN"

# Wrap and send
jq '{engineering_plan: .}' "$LATEST_PLAN" | \
curl -X POST http://localhost:5678/webhook/planning-agent/project-schedule \
  -H "Content-Type: application/json" \
  -d @- | jq '.'
```

### Direct Test with Manual Payload

```bash
cd /Users/udayammanagi/Udays-Folder/IK/brd_agent_em

# Read engineering plan and wrap it
PLAN_CONTENT=$(cat sample_inputs/outputs/engineering_plans/engineering_plan_customer_onboarding_and_success_portal_cosp_brd_v1_2025-11-15T15-07-55.json)

# Send wrapped payload
curl -X POST http://localhost:5678/webhook/planning-agent/project-schedule \
  -H "Content-Type: application/json" \
  -d "{\"engineering_plan\": $PLAN_CONTENT}" | jq '.'
```

---

## 📊 Expected Output

### Success Response
```json
{
  "status": "success",
  "message": "Project schedule generated successfully",
  "filename": "project_schedule_customer_onboarding_and_success_portal_cosp_brd_v1_2025-11-15T15-30-00.json",
  "filepath": "/data/projects/IK/brd_agent_em/sample_inputs/outputs/project_schedules/project_schedule_customer_onboarding_and_success_portal_cosp_brd_v1_2025-11-15T15-30-00.json"
}
```

### Output File Structure
```json
{
  "project_schedule": {
    "project_info": {
      "project_name": "Customer Onboarding and Success Portal",
      "start_date": "2025-11-15",
      "estimated_end_date": "2026-05-15",
      "total_duration_weeks": 26,
      "total_effort_person_weeks": 180
    },
    "phases": [...],
    "resource_allocation": [...],
    "critical_path": [...],
    "risk_timeline": [...],
    "key_deliverables": [...]
  }
}
```

### Generated Files Location
```
sample_inputs/outputs/project_schedules/
└── project_schedule_customer_onboarding_and_success_portal_cosp_brd_v1_2025-11-15T15-30-00.json
```

---

## ❌ Troubleshooting

### Error: "Workflow not found"
- Make sure the workflow is imported and **activated** in n8n
- Check the toggle switch is ON (blue) in n8n UI

### Error: "engineering_plan is required"
- The payload needs to be wrapped: `{"engineering_plan": {...}}`
- Use the `jq` wrapper command or test script

### Error: "Invalid Engineering Plan format"
- Make sure you're passing a valid engineering plan JSON
- Check the file isn't double-wrapped or corrupted

### Error: "ENOENT: no such file or directory"
- Verify Docker is running with the correct volume mount
- Check `docker-compose.yml` has: `/Users/udayammanagi/Udays-Folder:/data/projects`

### Error: "Anthropic API error"
- Verify your Anthropic API key is configured in n8n credentials
- Check your API quota/billing status

---

## 🔄 Complete End-to-End Test

### Full Pipeline Test (BRD → Engineering Plan → Schedule)

```bash
cd /Users/udayammanagi/Udays-Folder/IK/brd_agent_em

# Step 1: Generate Engineering Plan
echo "📝 Step 1: Generating Engineering Plan..."
curl -s -X POST http://localhost:5678/webhook/planning-agent/engineering-plan \
  -H "Content-Type: application/json" \
  -d @sample_inputs/brds/brd_input_cleaner.json \
  -o /tmp/current_eng_plan.json

echo "✅ Engineering plan generated"
cat /tmp/current_eng_plan.json | jq '.'

# Step 2: Generate Project Schedule
echo ""
echo "🗓️ Step 2: Generating Project Schedule..."
jq '{engineering_plan: .}' /tmp/current_eng_plan.json | \
curl -s -X POST http://localhost:5678/webhook/planning-agent/project-schedule \
  -H "Content-Type: application/json" \
  -d @- | jq '.'

# Step 3: View outputs
echo ""
echo "📁 Generated Files:"
echo ""
echo "Engineering Plans:"
ls -lht sample_inputs/outputs/engineering_plans/ | head -3
echo ""
echo "Project Schedules:"
ls -lht sample_inputs/outputs/project_schedules/ | head -3
```

---

## 📈 What to Validate

After running the test, verify:

1. ✅ **Workflow Executes Successfully**
   - No errors in n8n execution log
   - All nodes show green checkmarks

2. ✅ **File Created**
   - Check `sample_inputs/outputs/project_schedules/`
   - Filename includes BRD name and version

3. ✅ **JSON Structure**
   - Open the generated file
   - Verify all sections are present
   - Check dates are realistic and sequential

4. ✅ **Content Quality**
   - Phases match engineering plan
   - Tasks have dependencies
   - Resource allocation is detailed
   - Critical path is identified

---

## 🎯 Next Steps After Testing

1. **Test with Multiple BRDs**
   - Add more sample BRDs to `sample_inputs/brds/`
   - Run end-to-end tests for each

2. **Validate Schedule Quality**
   - Review generated timelines
   - Check if dependencies make sense
   - Verify resource allocations are realistic

3. **Build Design Agent**
   - Architecture Generator
   - PoC Document Generator
   - Tech Stack Recommendations

4. **Chain Everything Together**
   - Master Orchestrator workflow
   - Full automation: BRD → Plan → Schedule → Design

---

**Ready to test? Start with the Quick Test Command above!** 🚀

