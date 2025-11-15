#!/bin/bash

# Test Project Schedule Generator
# Usage: ./test_schedule_generator.sh <path-to-engineering-plan.json>

ENGINEERING_PLAN_FILE="$1"
N8N_URL="http://localhost:5678/webhook/planning-agent/project-schedule"

if [ -z "$ENGINEERING_PLAN_FILE" ]; then
  echo "🗓️  Project Schedule Generator - Test Script"
  echo ""
  echo "Usage: tests/integration/test_schedule_generator.sh <path-to-engineering-plan.json>"
  echo ""
  echo "Examples (run from project root):"
  echo "  # Test with latest engineering plan"
  echo "  tests/integration/test_schedule_generator.sh \$(ls -t sample_inputs/outputs/engineering_plans/*.json | head -1)"
  echo ""
  echo "  # Test with specific file"
  echo "  tests/integration/test_schedule_generator.sh sample_inputs/outputs/engineering_plans/engineering_plan_customer_onboarding_and_success_portal_cosp_brd_v1_2025-11-15T15-07-55.json"
  exit 1
fi

if [ ! -f "$ENGINEERING_PLAN_FILE" ]; then
  echo "❌ Error: File not found: $ENGINEERING_PLAN_FILE"
  exit 1
fi

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "❌ Error: jq is not installed"
    echo "Install with: brew install jq"
    exit 1
fi

echo "🧪 Testing Project Schedule Generator"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📄 Input: $(basename $ENGINEERING_PLAN_FILE)"
echo "🔗 Endpoint: $N8N_URL"
echo ""

# Wrap the engineering plan in the expected format
echo "⏳ Preparing payload..."
WRAPPED_PAYLOAD=$(jq '{engineering_plan: .}' "$ENGINEERING_PLAN_FILE")

if [ $? -ne 0 ]; then
  echo "❌ Error: Failed to parse engineering plan JSON"
  exit 1
fi

# Send request
echo "⏳ Sending request to n8n..."
RESPONSE=$(echo "$WRAPPED_PAYLOAD" | curl -s -w "\n%{http_code}" -X POST "$N8N_URL" \
  -H "Content-Type: application/json" \
  -d @-)

# Extract HTTP status code (last line)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$RESPONSE" | sed '$d')

echo ""
if [ "$HTTP_CODE" = "200" ]; then
  echo "✅ Success! (HTTP $HTTP_CODE)"
  echo ""
  echo "Response:"
  echo "$RESPONSE_BODY" | jq '.'
  
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "📁 Generated Schedule Files:"
  echo ""
  ls -lht sample_inputs/outputs/project_schedules/ 2>/dev/null | head -6 || echo "No files found yet"
  
  echo ""
  echo "🎉 Test completed successfully!"
else
  echo "❌ Error! (HTTP $HTTP_CODE)"
  echo ""
  echo "Response:"
  echo "$RESPONSE_BODY"
  
  echo ""
  echo "💡 Troubleshooting tips:"
  echo "  1. Check if workflow is activated in n8n"
  echo "  2. Verify Anthropic API credentials are configured"
  echo "  3. Check n8n logs for detailed error"
fi

