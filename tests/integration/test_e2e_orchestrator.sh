#!/bin/bash

# End-to-End Test Script for Master Orchestrator
# Tests: PDF → Parser → Engineering Plan → Schedule

set -e  # Exit on error

echo "🚀 End-to-End Orchestrator Test"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Configuration
N8N_URL="http://localhost:5678"
BRD_PARSER_URL="http://localhost:8000"
ORCHESTRATOR_URL="$N8N_URL/webhook/orchestrator/process-brd-v2"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# Check prerequisites
echo "📋 Checking prerequisites..."
echo ""

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    print_error "jq is not installed. Install with: brew install jq"
    exit 1
fi
print_status "jq installed"

# Check if docker is running
if ! docker ps &> /dev/null; then
    print_error "Docker is not running. Start with: docker-compose up -d"
    exit 1
fi
print_status "Docker is running"

# Check if n8n is accessible
if ! curl -s "$N8N_URL" > /dev/null; then
    print_error "n8n is not accessible at $N8N_URL"
    exit 1
fi
print_status "n8n is accessible"

# Check if BRD Parser is accessible
if ! curl -s "$BRD_PARSER_URL/health" > /dev/null; then
    print_error "BRD Parser is not accessible at $BRD_PARSER_URL"
    print_info "Start with: docker-compose up -d brd-parser"
    exit 1
fi
print_status "BRD Parser is accessible"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test input
INPUT_FILE="$1"

if [ -z "$INPUT_FILE" ]; then
    print_info "No input file specified"
    print_info "Usage: $0 <path-to-brd.json-or-pdf>"
    echo ""
    print_info "Testing with sample JSON BRD data..."
    echo ""
    
    # Create sample BRD data
    INPUT_DATA=$(cat <<'EOF'
{
  "brd_data": {
    "project": {
      "name": "E-Commerce Platform",
      "description": "A modern e-commerce platform with user management, product catalog, and checkout",
      "objectives": [
        "Provide seamless shopping experience",
        "Enable easy product management",
        "Secure payment processing"
      ],
      "constraints": [
        "Must support 10,000 concurrent users",
        "PCI DSS compliance required",
        "Mobile-first design"
      ]
    },
    "features": [
      {
        "id": "F001",
        "name": "User Authentication",
        "description": "Secure user registration and login",
        "priority": "High",
        "requirements": [
          "Email/password authentication",
          "OAuth2 social login",
          "Password reset flow",
          "Two-factor authentication"
        ]
      },
      {
        "id": "F002",
        "name": "Product Catalog",
        "description": "Browse and search products",
        "priority": "High",
        "requirements": [
          "Product listing with pagination",
          "Advanced search and filters",
          "Product details page",
          "Image gallery"
        ]
      },
      {
        "id": "F003",
        "name": "Shopping Cart",
        "description": "Add products to cart and manage",
        "priority": "High",
        "requirements": [
          "Add/remove items",
          "Update quantities",
          "Save cart for later",
          "Apply promo codes"
        ]
      }
    ],
    "stakeholders": [
      "Product Management",
      "Engineering Team",
      "Marketing",
      "Customer Support"
    ],
    "technical_requirements": {
      "platforms": ["Web", "Mobile (iOS/Android)"],
      "integrations": ["Stripe", "SendGrid", "Google Analytics"],
      "performance": "Page load under 2 seconds",
      "security": "PCI DSS compliant, HTTPS only",
      "scalability": "Support 10K concurrent users"
    },
    "success_criteria": [
      "User registration completion rate > 80%",
      "Cart abandonment rate < 30%",
      "Page load time < 2 seconds",
      "99.9% uptime"
    ]
  }
}
EOF
)
else
    if [ ! -f "$INPUT_FILE" ]; then
        print_error "File not found: $INPUT_FILE"
        exit 1
    fi
    
    print_info "Using input file: $INPUT_FILE"
    
    # Check file type
    if [[ "$INPUT_FILE" == *.pdf ]]; then
        print_info "PDF file detected - will be parsed by BRD Parser"
        # TODO: Add PDF upload logic
        print_error "PDF upload not yet implemented in this script"
        exit 1
    else
        # Assume JSON
        INPUT_DATA=$(cat "$INPUT_FILE")
    fi
fi

echo ""
echo "🔄 Starting End-to-End Test..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Send request to orchestrator
print_info "Sending request to Master Orchestrator..."
START_TIME=$(date +%s)

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$ORCHESTRATOR_URL" \
  -H "Content-Type: application/json" \
  -d "$INPUT_DATA")

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# Extract HTTP status code
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$RESPONSE" | sed '$d')

echo ""

if [ "$HTTP_CODE" = "200" ]; then
    # Validate response body is not empty
    if [ -z "$RESPONSE_BODY" ] || [ "$RESPONSE_BODY" = "{}" ]; then
        print_error "Orchestration returned HTTP 200 but response body is empty!"
        print_error "This usually means workflows are not properly activated in n8n."
        echo ""
        print_error "❌ END-TO-END TEST FAILED (Empty Response)"
        echo ""
        exit 1
    fi
    
    # Validate response has status field
    RESPONSE_STATUS=$(echo "$RESPONSE_BODY" | jq -r '.status // empty')
    if [ -z "$RESPONSE_STATUS" ]; then
        print_error "Orchestration returned HTTP 200 but response has no .status field!"
        echo ""
        echo "Response received:"
        echo "$RESPONSE_BODY"
        echo ""
        print_error "❌ END-TO-END TEST FAILED (Invalid Response)"
        echo ""
        exit 1
    fi
    
    # Validate orchestration succeeded
    if [ "$RESPONSE_STATUS" != "success" ]; then
        print_error "Orchestration status: $RESPONSE_STATUS"
        echo ""
        echo "Response:"
        echo "$RESPONSE_BODY" | jq '.'
        echo ""
        print_error "❌ END-TO-END TEST FAILED (Orchestration Failed)"
        echo ""
        exit 1
    fi
    
    print_status "Orchestration completed successfully! (HTTP $HTTP_CODE)"
    print_info "Duration: ${DURATION} seconds"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📊 Results:"
    echo ""
    
    # Parse and display simplified results
    RESULT_SUMMARY=$(echo "$RESPONSE_BODY" | jq '{
      status: .status,
      message: .message,
      stages_completed: .stages_completed,
      timestamp: .timestamp,
      note: .note
    }')
    
    if [ $? -ne 0 ] || [ -z "$RESULT_SUMMARY" ]; then
        print_error "Failed to parse response results!"
        echo ""
        echo "Raw response:"
        echo "$RESPONSE_BODY"
        echo ""
        print_error "❌ END-TO-END TEST FAILED (Parse Error)"
        echo ""
        exit 1
    fi
    
    echo "$RESULT_SUMMARY"
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    print_status "All stages completed:"
    echo "$RESPONSE_BODY" | jq -r '.stages_completed[] | "  ✓ " + .'
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    print_info "Full response saved to: /tmp/orchestrator_test_response.json"
    echo "$RESPONSE_BODY" | jq '.' > /tmp/orchestrator_test_response.json
    
    echo ""
    print_status "✅ END-TO-END TEST PASSED!"
    echo ""
    
else
    print_error "Orchestration failed! (HTTP $HTTP_CODE)"
    echo ""
    echo "Response:"
    echo "$RESPONSE_BODY" | jq '.' || echo "$RESPONSE_BODY"
    echo ""
    print_error "❌ END-TO-END TEST FAILED"
    echo ""
    exit 1
fi

# Check generated files
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
print_info "Checking generated output files..."
echo ""

if [ -d "sample_inputs/outputs/engineering_plans" ]; then
    PLAN_COUNT=$(ls -1 sample_inputs/outputs/engineering_plans/*.json 2>/dev/null | wc -l)
    print_status "Engineering Plans: $PLAN_COUNT files"
    ls -lht sample_inputs/outputs/engineering_plans/*.json 2>/dev/null | head -3
fi

echo ""

if [ -d "sample_inputs/outputs/project_schedules" ]; then
    SCHEDULE_COUNT=$(ls -1 sample_inputs/outputs/project_schedules/*.json 2>/dev/null | wc -l)
    print_status "Project Schedules: $SCHEDULE_COUNT files"
    ls -lht sample_inputs/outputs/project_schedules/*.json 2>/dev/null | head -3
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
print_status "🎉 Complete end-to-end pipeline tested successfully!"
echo ""

