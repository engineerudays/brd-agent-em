# Planning Agent - Test Requests

This file contains sample API requests for testing the Planning Agent workflows.

## 🧪 Test Engineering Plan Generator

### Sample Request 1: Using Parsed BRD

```bash
curl -X POST http://localhost:5678/webhook/planning-agent/engineering-plan \
  -H "Content-Type: application/json" \
  -d @- << 'EOF'
{
  "raw_brd_text": "{\"document_info\":{\"title\":\"Customer Onboarding Portal\",\"version\":\"1.0\",\"status\":\"Draft\"},\"business_objectives\":[{\"id\":\"BO-01\",\"objective\":\"Reduce Customer Churn\",\"metric_success_criteria\":\"Decrease net churn rate by 5%\",\"priority\":\"Must\"},{\"id\":\"BO-02\",\"objective\":\"Improve Time-to-Value\",\"metric_success_criteria\":\"Reduce TTV from 30 to 14 days\",\"priority\":\"Must\"}],\"requirements\":{\"functional\":[{\"id\":\"FR-01\",\"description\":\"SSO login integration\",\"priority\":\"Critical\"},{\"id\":\"FR-02\",\"description\":\"Personalized onboarding checklist\",\"priority\":\"Critical\"}],\"non_functional\":[{\"id\":\"NFR-01\",\"description\":\"Page load under 2 seconds\",\"category\":\"Performance\",\"priority\":\"Critical\"}]},\"project_scope\":{\"in_scope\":[\"Self-service onboarding\",\"Knowledge base integration\",\"Usage analytics\"],\"out_of_scope\":[\"In-app product tours\",\"Ticketing system replacement\"]},\"constraints_assumptions_dependencies\":{\"constraints\":[\"Budget: $500,000\",\"Timeline: 6 months for MVP\"],\"assumptions\":[\"APIs are available\"],\"dependencies\":[\"Usage Data Pipeline team\"]}}"
}
EOF
```

### Sample Request 2: Minimal BRD

```bash
curl -X POST http://localhost:5678/webhook/planning-agent/engineering-plan \
  -H "Content-Type: application/json" \
  -d '{
    "raw_brd_text": "{\"document_info\":{\"title\":\"E-commerce Platform\"},\"business_objectives\":[{\"objective\":\"Increase sales\"}],\"requirements\":{\"functional\":[{\"description\":\"Product catalog\"}],\"non_functional\":[{\"description\":\"Fast loading\"}]}}"
  }'
```

### Expected Response Format

```json
{
  "engineering_plan": {
    "project_overview": {
      "name": "Customer Onboarding Portal",
      "description": "A self-service platform for customer onboarding...",
      "objectives": [
        "Reduce customer churn by 5%",
        "Improve time-to-value from 30 to 14 days"
      ]
    },
    "feature_breakdown": [
      {
        "feature_id": "F001",
        "feature_name": "SSO Integration",
        "description": "Single Sign-On with main SaaS product",
        "priority": "Critical",
        "complexity": "Medium",
        "estimated_effort": "2 weeks",
        "dependencies": [],
        "technical_requirements": [
          "OAuth 2.0 implementation",
          "JWT token handling"
        ],
        "acceptance_criteria": [
          "Users can log in with existing credentials",
          "Session persists across applications"
        ]
      }
    ],
    "technical_architecture": {
      "system_components": [
        "Frontend React Application",
        "Backend API Gateway",
        "Authentication Service",
        "Database"
      ],
      "integration_points": [
        "Main SaaS Product API",
        "CRM (Salesforce)",
        "Knowledge Base API"
      ],
      "data_flow": "User authenticates -> Portal loads -> Data fetched from APIs",
      "security_considerations": [
        "TLS 1.2+ encryption",
        "ISO 27001 compliance",
        "API rate limiting"
      ]
    },
    "implementation_phases": [
      {
        "phase_number": 1,
        "phase_name": "MVP - Core Features",
        "description": "Essential functionality for launch",
        "features_included": ["SSO", "Basic Dashboard"],
        "estimated_duration": "8 weeks",
        "deliverables": ["Working authentication", "Basic UI"]
      }
    ],
    "risk_analysis": [
      {
        "risk_id": "R001",
        "description": "Third-party API availability",
        "impact": "High",
        "probability": "Medium",
        "mitigation_strategy": "Implement fallback mechanisms and caching"
      }
    ],
    "resource_requirements": {
      "team_composition": [
        "1 Tech Lead",
        "2 Full-stack Developers",
        "1 UI/UX Designer",
        "1 QA Engineer"
      ],
      "tools_and_technologies": [
        "React",
        "Node.js",
        "PostgreSQL",
        "AWS"
      ],
      "infrastructure_needs": [
        "Cloud hosting",
        "CI/CD pipeline",
        "Monitoring tools"
      ]
    },
    "success_metrics": [
      {
        "metric_name": "Customer Churn Rate",
        "target_value": "5% reduction",
        "measurement_method": "Monthly cohort analysis"
      }
    ]
  },
  "metadata": {
    "generated_by": "Planning Agent - Engineering Plan Generator",
    "timestamp": "2025-11-11T10:30:00.000Z",
    "source_brd": "Customer Onboarding Portal",
    "version": "1.0"
  }
}
```

## 🧪 Test Project Schedule Generator

### Sample Request: Using Engineering Plan

```bash
curl -X POST http://localhost:5678/webhook/planning-agent/project-schedule \
  -H "Content-Type: application/json" \
  -d @- << 'EOF'
{
  "engineering_plan": {
    "project_overview": {
      "name": "Customer Onboarding Portal",
      "description": "Self-service onboarding platform",
      "objectives": ["Reduce churn", "Improve TTV"]
    },
    "feature_breakdown": [
      {
        "feature_id": "F001",
        "feature_name": "SSO Integration",
        "priority": "Critical",
        "complexity": "Medium",
        "estimated_effort": "2 weeks",
        "dependencies": []
      },
      {
        "feature_id": "F002",
        "feature_name": "Dashboard",
        "priority": "High",
        "complexity": "Medium",
        "estimated_effort": "3 weeks",
        "dependencies": ["F001"]
      }
    ],
    "implementation_phases": [
      {
        "phase_number": 1,
        "phase_name": "MVP",
        "features_included": ["F001", "F002"],
        "estimated_duration": "8 weeks"
      }
    ],
    "risk_analysis": [
      {
        "risk_id": "R001",
        "description": "API availability",
        "impact": "High",
        "probability": "Medium"
      }
    ],
    "resource_requirements": {
      "team_composition": ["Tech Lead", "2 Developers", "1 Designer"],
      "tools_and_technologies": ["React", "Node.js"],
      "infrastructure_needs": ["AWS"]
    }
  }
}
EOF
```

### Expected Response Format

```json
{
  "success": true,
  "project_schedule": {
    "project_info": {
      "project_name": "Customer Onboarding Portal",
      "start_date": "2025-11-11",
      "estimated_end_date": "2026-01-06",
      "total_duration_weeks": 8,
      "total_effort_person_weeks": 20
    },
    "phases": [
      {
        "phase_id": "P001",
        "phase_name": "MVP - Core Features",
        "start_date": "2025-11-11",
        "end_date": "2026-01-06",
        "duration_weeks": 8,
        "milestones": [
          {
            "milestone_id": "M001",
            "name": "SSO Integration Complete",
            "target_date": "2025-11-25",
            "deliverables": [
              "Working authentication",
              "JWT implementation"
            ],
            "dependencies": []
          },
          {
            "milestone_id": "M002",
            "name": "Dashboard Launch",
            "target_date": "2025-12-16",
            "deliverables": [
              "User dashboard",
              "Analytics integration"
            ],
            "dependencies": ["M001"]
          }
        ],
        "tasks": [
          {
            "task_id": "T001",
            "task_name": "Setup OAuth 2.0",
            "description": "Implement OAuth flow with main product",
            "assigned_to": "Backend Developer",
            "start_date": "2025-11-11",
            "end_date": "2025-11-18",
            "effort_days": 5,
            "status": "Not Started",
            "dependencies": [],
            "priority": "Critical"
          },
          {
            "task_id": "T002",
            "task_name": "Design Dashboard UI",
            "description": "Create wireframes and mockups",
            "assigned_to": "UI/UX Designer",
            "start_date": "2025-11-11",
            "end_date": "2025-11-15",
            "effort_days": 3,
            "status": "Not Started",
            "dependencies": [],
            "priority": "High"
          },
          {
            "task_id": "T003",
            "task_name": "Implement Dashboard",
            "description": "Build React dashboard components",
            "assigned_to": "Frontend Developer",
            "start_date": "2025-11-18",
            "end_date": "2025-12-09",
            "effort_days": 15,
            "status": "Not Started",
            "dependencies": ["T001", "T002"],
            "priority": "High"
          }
        ]
      }
    ],
    "resource_allocation": [
      {
        "role": "Tech Lead",
        "allocation_percentage": 50,
        "start_date": "2025-11-11",
        "end_date": "2026-01-06",
        "key_responsibilities": [
          "Architecture decisions",
          "Code reviews",
          "Team coordination"
        ]
      },
      {
        "role": "Full-stack Developer",
        "allocation_percentage": 100,
        "start_date": "2025-11-11",
        "end_date": "2026-01-06",
        "key_responsibilities": [
          "Feature implementation",
          "API integration",
          "Testing"
        ]
      }
    ],
    "critical_path": [
      {
        "task_id": "T001",
        "task_name": "Setup OAuth 2.0",
        "duration_days": 5,
        "slack_days": 0
      },
      {
        "task_id": "T003",
        "task_name": "Implement Dashboard",
        "duration_days": 15,
        "slack_days": 0
      }
    ],
    "risk_timeline": [
      {
        "risk_id": "R001",
        "description": "Third-party API availability",
        "impact_on_schedule": "Could delay integration by 1-2 weeks",
        "contingency_buffer_days": 5
      }
    ],
    "key_deliverables": [
      {
        "deliverable_name": "SSO Authentication Module",
        "due_date": "2025-11-25",
        "responsible_team": "Backend Team",
        "dependencies": []
      },
      {
        "deliverable_name": "User Dashboard",
        "due_date": "2025-12-16",
        "responsible_team": "Frontend Team",
        "dependencies": ["SSO Authentication Module"]
      }
    ],
    "assumptions": [
      "All team members available full-time",
      "APIs are stable and documented",
      "No major scope changes during development"
    ],
    "constraints": [
      "Budget: $500,000",
      "MVP must launch within 8 weeks",
      "Must use RESTful APIs for integrations"
    ]
  },
  "summary": {
    "total_phases": 1,
    "total_tasks": 3,
    "total_milestones": 2,
    "generated_at": "2025-11-11T10:45:00.000Z"
  },
  "visualization": {
    "gantt_chart": {
      "chart_type": "gantt",
      "project_name": "Customer Onboarding Portal",
      "start_date": "2025-11-11",
      "end_date": "2026-01-06",
      "tasks": [
        {
          "id": "phase-0",
          "name": "MVP - Core Features",
          "start": "2025-11-11",
          "end": "2026-01-06",
          "type": "phase",
          "progress": 0,
          "dependencies": []
        },
        {
          "id": "T001",
          "name": "Setup OAuth 2.0",
          "start": "2025-11-11",
          "end": "2025-11-18",
          "type": "task",
          "progress": 0,
          "dependencies": [],
          "assigned_to": "Backend Developer",
          "priority": "Critical",
          "parent": "phase-0"
        },
        {
          "id": "T002",
          "name": "Design Dashboard UI",
          "start": "2025-11-11",
          "end": "2025-11-15",
          "type": "task",
          "progress": 0,
          "dependencies": [],
          "assigned_to": "UI/UX Designer",
          "priority": "High",
          "parent": "phase-0"
        },
        {
          "id": "T003",
          "name": "Implement Dashboard",
          "start": "2025-11-18",
          "end": "2025-12-09",
          "type": "task",
          "progress": 0,
          "dependencies": ["T001", "T002"],
          "assigned_to": "Frontend Developer",
          "priority": "High",
          "parent": "phase-0"
        }
      ],
      "generated_at": "2025-11-11T10:45:00.000Z"
    }
  },
  "metadata": {
    "generated_by": "Planning Agent - Project Schedule Generator",
    "timestamp": "2025-11-11T10:45:00.000Z",
    "source_plan": "Customer Onboarding Portal",
    "version": "1.0"
  }
}
```

## 🔗 Chained Test (End-to-End)

### Step 1: Generate Engineering Plan

```bash
# Save response to file
curl -X POST http://localhost:5678/webhook/planning-agent/engineering-plan \
  -H "Content-Type: application/json" \
  -d '{"raw_brd_text": "{...BRD_JSON...}"}' \
  > engineering_plan_output.json
```

### Step 2: Generate Project Schedule from Plan

```bash
# Use the output from step 1
curl -X POST http://localhost:5678/webhook/planning-agent/project-schedule \
  -H "Content-Type: application/json" \
  -d @engineering_plan_output.json \
  > project_schedule_output.json
```

## 🧰 Testing Tools

### Using Postman

1. Import these requests as a Postman collection
2. Set environment variable: `BASE_URL = http://localhost:5678`
3. Use `{{BASE_URL}}` in requests
4. Test each endpoint independently

### Using Python

```python
import requests
import json

# Test Engineering Plan Generator
brd_data = {
    "raw_brd_text": json.dumps({
        "document_info": {"title": "Test Project"},
        "business_objectives": [{"objective": "Test objective"}],
        "requirements": {"functional": [], "non_functional": []}
    })
}

response = requests.post(
    "http://localhost:5678/webhook/planning-agent/engineering-plan",
    json=brd_data
)

plan = response.json()
print("Engineering Plan:", json.dumps(plan, indent=2))

# Test Schedule Generator with the plan
schedule_response = requests.post(
    "http://localhost:5678/webhook/planning-agent/project-schedule",
    json={"engineering_plan": plan["engineering_plan"]}
)

schedule = schedule_response.json()
print("Project Schedule:", json.dumps(schedule, indent=2))
```

### Using Node.js

```javascript
const axios = require('axios');

async function testPlanningAgent() {
  // Generate Engineering Plan
  const brdResponse = await axios.post(
    'http://localhost:5678/webhook/planning-agent/engineering-plan',
    {
      raw_brd_text: JSON.stringify({
        document_info: { title: 'Test Project' },
        business_objectives: [{ objective: 'Test' }],
        requirements: { functional: [], non_functional: [] }
      })
    }
  );
  
  console.log('Engineering Plan:', brdResponse.data);
  
  // Generate Schedule
  const scheduleResponse = await axios.post(
    'http://localhost:5678/webhook/planning-agent/project-schedule',
    {
      engineering_plan: brdResponse.data.engineering_plan
    }
  );
  
  console.log('Project Schedule:', scheduleResponse.data);
}

testPlanningAgent();
```

## ❌ Error Cases to Test

### Invalid BRD Format
```bash
curl -X POST http://localhost:5678/webhook/planning-agent/engineering-plan \
  -H "Content-Type: application/json" \
  -d '{"raw_brd_text": "not valid json"}'
```

Expected: 400 error with message about invalid format

### Missing Required Fields
```bash
curl -X POST http://localhost:5678/webhook/planning-agent/engineering-plan \
  -H "Content-Type: application/json" \
  -d '{}'
```

Expected: 400 error about missing raw_brd_text

### Empty Engineering Plan
```bash
curl -X POST http://localhost:5678/webhook/planning-agent/project-schedule \
  -H "Content-Type: application/json" \
  -d '{"engineering_plan": {}}'
```

Expected: Should handle gracefully with minimal schedule

## 📊 Performance Testing

### Load Test with Apache Bench
```bash
# Test 100 requests with 10 concurrent
ab -n 100 -c 10 -p brd_payload.json -T application/json \
  http://localhost:5678/webhook/planning-agent/engineering-plan
```

### Measure Response Time
```bash
time curl -X POST http://localhost:5678/webhook/planning-agent/engineering-plan \
  -H "Content-Type: application/json" \
  -d @sample_brd.json
```

---

**Note:** Replace `localhost:5678` with your actual n8n instance URL and port.


==============================================================
ROUGH TEST CASES

curl -X POST http://localhost:5678/webhook-test/planning-agent/engineering-plan \
  -H "Content-Type: application/json" \
  -d @sample_inputs/brds/brd_input_cleaner.json

