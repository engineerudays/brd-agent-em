# Planning Agent Workflows - Implementation Guide

## 📋 Overview

This directory contains two n8n workflows for the Planning Agent that transform Business Requirements Documents (BRDs) into actionable engineering plans and project schedules.

## 🔧 Available Workflows

### 1. Structured Engineering Plan Generator
**File:** `engineering_plan/structured_plan_generator.json`

**Purpose:** Transforms parsed BRD data into a comprehensive engineering plan with technical details, feature breakdown, and implementation phases.

**Input:** Parsed BRD JSON (from BRD Parser)
**Output:** Structured Engineering Plan with:
- Project overview and objectives
- Feature breakdown with priorities and effort estimates
- Technical architecture components
- Implementation phases
- Risk analysis
- Resource requirements
- Success metrics

**Webhook Endpoint:** `/planning-agent/engineering-plan`

### 2. Project Schedule Generator
**File:** `project_schedule/project_schedule_generator.json`

**Purpose:** Creates detailed project schedules with timelines, milestones, and Gantt chart data based on the engineering plan.

**Input:** Engineering Plan JSON (from Structured Engineering Plan Generator)
**Output:** Project Schedule with:
- Project timeline with start/end dates
- Phase breakdown with milestones
- Detailed tasks with dependencies
- Resource allocation
- Critical path analysis
- Risk timeline
- Gantt chart visualization data

**Webhook Endpoint:** `/planning-agent/project-schedule`

## 🚀 How to Import into n8n

### Step 1: Import Workflows

1. Open your n8n instance
2. Navigate to **Workflows** → **Import**
3. Import both JSON files:
   - `engineering_plan/structured_plan_generator.json`
   - `project_schedule/project_schedule_generator.json`

### Step 2: Configure AI Credentials

Both workflows use OpenAI for AI generation. You need to:

1. Go to **Settings** → **Credentials**
2. Add **OpenAI API** credentials:
   - Name: `OpenAI API`
   - API Key: Your OpenAI API key
3. The workflows will automatically use these credentials

### Step 3: Activate Workflows

1. Open each imported workflow
2. Click **Active** toggle in the top-right corner
3. Save the workflow

## 📡 API Usage

### Engineering Plan Generation

**Request:**
```bash
curl -X POST http://your-n8n-instance/webhook/planning-agent/engineering-plan \
  -H "Content-Type: application/json" \
  -d '{
    "raw_brd_text": "{\"document_info\": {...}, \"business_objectives\": [...], ...}"
  }'
```

**Response:**
```json
{
  "engineering_plan": {
    "project_overview": {...},
    "feature_breakdown": [...],
    "technical_architecture": {...},
    "implementation_phases": [...],
    "risk_analysis": [...],
    "resource_requirements": {...},
    "success_metrics": [...]
  },
  "metadata": {
    "generated_by": "Planning Agent - Engineering Plan Generator",
    "timestamp": "2025-11-11T...",
    "source_brd": "Customer Onboarding and Success Portal",
    "version": "1.0"
  }
}
```

### Project Schedule Generation

**Request:**
```bash
curl -X POST http://your-n8n-instance/webhook/planning-agent/project-schedule \
  -H "Content-Type: application/json" \
  -d '{
    "engineering_plan": {...}
  }'
```

**Response:**
```json
{
  "success": true,
  "project_schedule": {
    "project_info": {...},
    "phases": [...],
    "resource_allocation": [...],
    "critical_path": [...],
    "risk_timeline": [...],
    "key_deliverables": [...]
  },
  "summary": {
    "total_phases": 3,
    "total_tasks": 45,
    "total_milestones": 12
  },
  "visualization": {
    "gantt_chart": {...}
  },
  "metadata": {...}
}
}
```

## 🔄 Workflow Architecture

### Engineering Plan Generator Flow:
```
Webhook Trigger 
  ↓
Validate BRD Input 
  ↓
Parse BRD Data 
  ↓
AI - Generate Engineering Plan (GPT-4)
  ↓
Format Engineering Plan Output 
  ↓
Save to State 
  ↓
Respond with Engineering Plan
```

### Project Schedule Generator Flow:
```
Webhook Trigger 
  ↓
Validate Engineering Plan 
  ↓
Parse Engineering Plan 
  ↓
AI - Generate Project Schedule (GPT-4)
  ↓
Format Schedule Output 
  ↓
Generate Gantt Chart Data 
  ↓
Save to State 
  ↓
Merge Final Output 
  ↓
Respond with Schedule
```

## 🎯 Key Features

### Intelligent Parsing
- Validates input data structure
- Handles both string and JSON inputs
- Graceful error handling with detailed messages

### AI-Powered Generation
- Uses GPT-4 for high-quality outputs
- Structured prompts for consistent results
- Configurable temperature and token limits

### State Management
- Saves latest engineering plan to n8n state
- Saves latest project schedule to n8n state
- Enables workflow chaining and history tracking

### Visualization Support
- Generates Gantt chart compatible data
- Includes task dependencies
- Progress tracking support

### Error Handling
- Comprehensive validation at each step
- Detailed error messages with timestamps
- Graceful fallback for parsing failures

## 🔗 Integration with Other Agents

### Upstream (Input):
- **BRD Parser** → Engineering Plan Generator

### Downstream (Output):
- Engineering Plan Generator → **Project Schedule Generator**
- Engineering Plan Generator → **Design Agent** (Architecture)
- Project Schedule → **Frontend Dashboard**
- Project Schedule → **Project Management Tools**

## 🛠️ Customization

### Modify AI Prompts

To customize the AI generation, edit the prompt in the "AI - Generate..." nodes:

1. Open the workflow
2. Click on the AI node (green)
3. Edit the `messages.values[0].content` field
4. Adjust temperature (0.0-1.0) for more/less creative outputs
5. Adjust maxTokens for longer/shorter responses

### Add Custom Processing

You can add custom JavaScript processing by:

1. Adding a new **Code** node
2. Writing custom JavaScript
3. Connecting it in the workflow chain

### Extend State Management

To save additional data:

1. Add a new **Set** node
2. Configure key-value pairs
3. Use `={{JSON.stringify($json)}}` for complex data

## 📊 Output Schema

### Engineering Plan Schema

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
        "feature_id": "string",
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
        "risk_id": "string",
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
  }
}
```

### Project Schedule Schema

```json
{
  "project_schedule": {
    "project_info": {
      "project_name": "string",
      "start_date": "YYYY-MM-DD",
      "estimated_end_date": "YYYY-MM-DD",
      "total_duration_weeks": 24,
      "total_effort_person_weeks": 48
    },
    "phases": [
      {
        "phase_id": "string",
        "phase_name": "string",
        "start_date": "YYYY-MM-DD",
        "end_date": "YYYY-MM-DD",
        "duration_weeks": 8,
        "milestones": [
          {
            "milestone_id": "string",
            "name": "string",
            "target_date": "YYYY-MM-DD",
            "deliverables": ["string"],
            "dependencies": ["string"]
          }
        ],
        "tasks": [
          {
            "task_id": "string",
            "task_name": "string",
            "description": "string",
            "assigned_to": "string",
            "start_date": "YYYY-MM-DD",
            "end_date": "YYYY-MM-DD",
            "effort_days": 5,
            "status": "Not Started",
            "dependencies": ["string"],
            "priority": "High"
          }
        ]
      }
    ],
    "resource_allocation": [...],
    "critical_path": [...],
    "risk_timeline": [...],
    "key_deliverables": [...]
  }
}
```

## ⚠️ Important Notes

1. **API Keys Required**: You must configure OpenAI API credentials before using these workflows
2. **Costs**: These workflows use GPT-4 which incurs API costs. Monitor your usage.
3. **Rate Limits**: Be aware of OpenAI rate limits for high-volume usage
4. **Webhook URLs**: Update webhook paths if you want custom endpoints
5. **State Storage**: n8n state is in-memory by default. For persistence, configure database storage

## 🐛 Troubleshooting

### Workflow doesn't trigger
- Check if workflow is **Active**
- Verify webhook URL is correct
- Check n8n logs for errors

### AI generation fails
- Verify OpenAI API key is valid
- Check API quota and limits
- Review prompt length (max tokens)

### Invalid output format
- Check input data structure
- Review error messages in response
- Validate JSON parsing in Code nodes

### State not saving
- Ensure Set nodes are connected
- Check n8n state configuration
- Review node execution logs

## 📚 Additional Resources

- [n8n Documentation](https://docs.n8n.io/)
- [OpenAI API Docs](https://platform.openai.com/docs/api-reference)
- [Project BRD Parser](../../brd_parser/README.md)
- [Design Agent Workflows](../design_agent/README.md)

## 🤝 Contributing

To modify or extend these workflows:

1. Import into n8n
2. Make your changes
3. Test thoroughly
4. Export the updated JSON
5. Replace the file in this directory
6. Update this README with changes
7. Commit to version control

---

**Version:** 1.0  
**Last Updated:** November 11, 2025  
**Maintainer:** BRD Agent Engineering System Team

