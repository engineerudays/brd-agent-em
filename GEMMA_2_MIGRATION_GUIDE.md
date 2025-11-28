# 🔄 Migration Guide: Claude Haiku → Gemma 2 (Local LLM)

## 📋 Overview

This guide provides a comprehensive roadmap for migrating the BRD Agent system from **Anthropic Claude 3 Haiku** (cloud API) to **Gemma 2** (locally hosted model). This migration eliminates API costs and keeps all data processing local while maintaining good quality output.

**Target Setup**: Gemma 2 9B running on Ollama (Docker or Native)

---

## 🎯 Migration Goals

- ✅ Eliminate API costs ($0.017/run → $0/run)
- ✅ Keep data processing 100% local
- ✅ Maintain 80-85% quality of Claude Haiku
- ✅ Achieve reasonable performance (60-90s total pipeline)
- ✅ Minimize code changes where possible

---

## ⚠️ Key Challenges & Solutions

### Challenge 1: Context Length Limitation
**Problem**: Gemma 2 has 8K token context, current usage is ~14.5K tokens

**Solutions**:
1. **Prompt Optimization** - Remove verbose schema examples (save ~2K tokens)
2. **Engineering Plan Summarization** - Extract only essential info before Schedule generation (save ~5K tokens)
3. **Two-stage approach** - Keep Engineering Plan verbose, summarize for Schedule

### Challenge 2: Quality Trade-off
**Expected**: 80-85% of Claude Haiku quality

**Mitigation**:
- Fine-tune prompts for Gemma's instruction style
- Add validation/retry logic for malformed JSON
- Test extensively with sample BRDs

### Challenge 3: Performance
**Expected**: 2-3x slower than Claude (60-90s vs 28-50s)

**Acceptable for**:
- Development/experimentation
- Low-volume usage (<100 runs/day)
- Privacy-sensitive use cases

---

## 💻 Hardware Requirements

### Minimum (for Gemma 2 9B):
- **CPU**: Apple M4 or equivalent x86_64
- **RAM**: 16GB (tight but workable)
- **Disk**: 20GB free space
- **OS**: macOS 14+, Ubuntu 20.04+, Windows 11 with WSL2

### Recommended:
- **RAM**: 32GB+ (comfortable headroom)
- **CPU**: 8+ cores
- **GPU**: Optional (10x speed boost with CUDA/Metal)

### Your Setup (M4 16GB):
- ✅ Will work
- ⚠️ Tight on memory (90% utilization expected)
- ⚠️ May need to close other apps during heavy usage
- ✅ M4 Neural Engine provides good acceleration

---

## 🏗️ Architecture Changes

### Current (v1.0.0 - Claude Haiku):
```
Streamlit UI → n8n (Docker) → Anthropic API (Cloud)
                  ↓
            BRD Parser (Docker) → Anthropic API (Cloud)
```

### Target (Gemma 2):
```
Streamlit UI → n8n (Docker) → Ollama (Native macOS) → Gemma 2 9B
                  ↓
            BRD Parser (Docker) → Ollama (Native macOS) → Gemma 2 9B
```

**Key Decision**: Run Ollama **natively** (not in Docker) for:
- Direct GPU/Neural Engine access
- Better memory management
- ~30% faster inference
- Docker containers connect via `host.docker.internal:11434`

---

## 📦 Infrastructure Setup

### Step 1: Install Ollama (Native macOS)

```bash
# Option A: Homebrew (Recommended)
brew install ollama

# Option B: Official installer
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version
```

### Step 2: Pull Gemma 2 9B Model

```bash
# Pull the model (4-5GB download)
ollama pull gemma2:9b

# Verify it's available
ollama list

# Test the model
ollama run gemma2:9b "Hello, how are you?"
```

### Step 3: Start Ollama Service

```bash
# Ollama runs automatically after installation
# To manually start if needed:
ollama serve

# Verify API is accessible
curl http://localhost:11434/api/tags
```

### Step 4: Update Docker Compose

**No changes needed!** Docker containers can access native Ollama via:
- URL: `http://host.docker.internal:11434`

---

## 🔧 Prompt Optimization Strategy

### Overview
Reduce token usage from ~14.5K to <8K while maintaining quality.

---

### Part 1: Engineering Plan Generator

**Current Token Usage**:
- BRD input: ~2,000 tokens
- Prompt + Schema: ~2,500 tokens
- Total input: ~4,500 tokens (✅ Fits in 8K)
- Output: ~4,000 tokens
- **Total: ~8,500 tokens** (⚠️ Slightly over)

**Optimization Target**: Reduce to ~7,500 tokens

#### Changes Needed:

**1. Simplify JSON Schema in Prompt**

**Current** (verbose):
```javascript
const prompt = `...
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
        "estimated_effort": "string (e.g., 2 weeks)",
        "dependencies": ["string"],
        "technical_requirements": ["string"],
        "acceptance_criteria": ["string"]
      }
    ],
    // ... more detailed schema ...
  }
}`;
```

**Optimized** (reference-based):
```javascript
const prompt = `...
Generate a JSON engineering plan with these sections:
- project_overview (name, description, objectives[])
- feature_breakdown[] (id, name, description, priority, complexity, effort, dependencies[], technical_requirements[], acceptance_criteria[])
- technical_architecture (components[], integrations[], data_flow, security[])
- implementation_phases[] (number, name, description, features[], duration, deliverables[])
- risk_analysis[] (id, description, impact, probability, mitigation)
- resource_requirements (team[], tools[], infrastructure[])
- success_metrics[] (name, target, measurement)

Return valid JSON only, no markdown.`;
```

**Savings**: ~1,000 tokens

---

**2. Reduce Instruction Verbosity**

**Current**:
```javascript
`IMPORTANT GUIDELINES:
1. Be EXTREMELY thorough and detailed in every section.
2. For each feature, provide comprehensive technical requirements and acceptance criteria (at least 2-4 items each).
3. Include specific technology mentions where appropriate (e.g., OAuth 2.0, SAML 2.0, React.js, Node.js, PostgreSQL, AWS EKS, etc.).
4. Ensure dependencies are clearly articulated.
5. Provide detailed risk mitigation strategies.
6. Specify team composition with roles and counts.
7. Outline detailed infrastructure needs.
8. Ensure implementation phases include clear deliverables and estimated durations.`
```

**Optimized**:
```javascript
`Be thorough and specific. Include technology names, dependencies, and realistic timelines.`
```

**Savings**: ~200 tokens

---

**3. Compress BRD Context (Optional)**

If BRD is very large (>6K tokens), extract only essential fields:
```javascript
const compressedBRD = {
  title: fullBRD.document_info?.title,
  objectives: fullBRD.business_objectives,
  requirements: fullBRD.requirements,
  scope: fullBRD.project_scope,
  constraints: fullBRD.constraints_assumptions_dependencies
};
```

**Savings**: Variable (0-1,000 tokens)

---

### Part 2: Project Schedule Generator

**Current Token Usage**:
- Engineering Plan input: ~8,000 tokens (❌ Major issue!)
- Prompt + Schema: ~2,500 tokens
- Total input: ~10,500 tokens (❌ Exceeds 8K!)
- Output: ~4,000 tokens
- **Total: ~14,500 tokens** (❌ Way over limit!)

**Optimization Target**: Reduce to ~7,500 tokens

#### Critical Change: Summarize Engineering Plan

**Add new node: "Summarize Engineering Plan for Scheduling"**

```javascript
// NEW NODE: Between "Parse Engineering Plan" and "Prepare AI Prompt"
// Purpose: Extract only scheduling-relevant data

const engineeringPlan = $input.item.json;

const schedulingSummary = {
  project_name: engineeringPlan.project_overview?.name,
  
  // Simplified phases (remove detailed descriptions)
  phases: engineeringPlan.implementation_phases?.map(phase => ({
    phase_id: phase.phase_number,
    phase_name: phase.phase_name,
    estimated_duration: phase.estimated_duration,
    features: phase.features_included || []
  })),
  
  // Simplified features (only essential scheduling info)
  features: engineeringPlan.feature_breakdown?.map(feature => ({
    id: feature.feature_id,
    name: feature.feature_name,
    priority: feature.priority,
    effort: feature.estimated_effort,
    dependencies: feature.dependencies || []
  })),
  
  // Key risks (top 5 only)
  risks: (engineeringPlan.risk_analysis || [])
    .sort((a, b) => {
      const impactOrder = { High: 3, Medium: 2, Low: 1 };
      return (impactOrder[b.impact] || 0) - (impactOrder[a.impact] || 0);
    })
    .slice(0, 5)
    .map(risk => ({
      id: risk.risk_id,
      description: risk.description,
      impact: risk.impact
    })),
  
  // Simplified resources
  resources: {
    team_size: engineeringPlan.resource_requirements?.team_composition?.length || 5,
    team_roles: engineeringPlan.resource_requirements?.team_composition?.slice(0, 5) || []
  },
  
  // Total estimated effort (if available)
  total_effort_estimate: engineeringPlan.implementation_phases?.reduce((sum, phase) => {
    const weeks = parseFloat(phase.estimated_duration) || 0;
    return sum + weeks;
  }, 0)
};

return { json: schedulingSummary };
```

**Savings**: ~5,000-6,000 tokens (reduces 8K plan to ~2K summary)

---

**Simplified Schedule Prompt**:

**Current**: Full schema with examples

**Optimized**:
```javascript
const prompt = `Create a project schedule based on this engineering plan summary:

${JSON.stringify(schedulingSummary, null, 2)}

Today's date: ${currentDate}

Generate JSON with:
- project_info (name, start_date, end_date, total_duration_weeks)
- phases[] (id, name, start_date, end_date, duration_weeks, tasks[], milestones[])
- resource_allocation[] (role, allocation%, start_date, end_date)
- critical_path[] (task_id, task_name, duration_days, slack_days)
- key_deliverables[] (name, due_date, team)

Tasks should include: id, name, assigned_to, start/end dates, effort_days, dependencies[], priority.
All dates in YYYY-MM-DD format. Return valid JSON only.`;
```

**Savings**: ~1,500 tokens

---

## 🔄 n8n Workflow Changes

### Engineering Plan Generator

**File**: `n8n_flows/planning_agent/engineering_plan/structured_plan_generator.json`

#### Changes Required:

**1. Update "Prepare AI Prompt" node**
- Simplify schema (remove detailed examples)
- Shorten instruction guidelines
- Keep same logic, just trim prompt text

**2. Update "AI - Generate Engineering Plan" HTTP Request node**

**Current**:
```json
{
  "method": "POST",
  "url": "https://api.anthropic.com/v1/messages",
  "authentication": "genericCredentialType",
  "genericAuthType": "httpHeaderAuth",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {
        "name": "anthropic-version",
        "value": "2023-06-01"
      }
    ]
  },
  "jsonBody": "={...}"
}
```

**New (Ollama)**:
```json
{
  "method": "POST",
  "url": "http://host.docker.internal:11434/v1/chat/completions",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {
        "name": "Content-Type",
        "value": "application/json"
      }
    ]
  },
  "jsonBody": "={\n  \"model\": \"gemma2:9b\",\n  \"messages\": [{\n    \"role\": \"user\",\n    \"content\": $json.prompt\n  }],\n  \"temperature\": 0.7,\n  \"max_tokens\": 4096\n}"
}
```

**3. Update "Format Engineering Plan Output" node**

Response format is slightly different:

**Anthropic**:
```javascript
const aiResponse = response.content?.[0]?.text || '';
```

**Ollama (OpenAI-compatible)**:
```javascript
const aiResponse = response.choices?.[0]?.message?.content || '';
```

---

### Project Schedule Generator

**File**: `n8n_flows/planning_agent/project_schedule/project_schedule_generator.json`

#### Changes Required:

**1. Add NEW node: "Summarize Engineering Plan"**
- Type: Code
- Position: Between "Parse Engineering Plan" and "Prepare AI Prompt"
- Code: See summarization logic above

**2. Update "Prepare AI Prompt" node**
- Use `schedulingSummary` instead of full plan
- Simplify schema
- Shorten instructions

**3. Update "AI - Generate Project Schedule" HTTP Request node**
- Same changes as Engineering Plan Generator
- Point to Ollama API
- Update response parsing

---

### BRD Parser Service (Optional)

**File**: `brd_parser/main.py`

If you want to use Gemma for BRD parsing too:

```python
# Current
from anthropic import Anthropic
anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)

# New (OpenAI-compatible client for Ollama)
from openai import OpenAI
ollama_client = OpenAI(
    base_url="http://host.docker.internal:11434/v1",
    api_key="not-needed"  # Ollama doesn't require API key
)

# Update API calls
response = ollama_client.chat.completions.create(
    model="gemma2:9b",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7,
    max_tokens=4096
)

extracted_text = response.choices[0].message.content
```

**Update `brd_parser/requirements.txt`**:
```
openai>=1.3.0  # Add this
anthropic>=0.74.0  # Can remove or keep for fallback
```

---

## 🧪 Testing & Validation

### Phase 1: Basic Functionality

**1. Test Ollama Installation**
```bash
# Test model directly
ollama run gemma2:9b "Generate a simple JSON object with 3 fields"

# Test API
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma2:9b",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

**2. Test from n8n Docker**
```bash
# Enter n8n container
docker exec -it brd_agent_em_n8n_1 /bin/sh

# Test connectivity
curl http://host.docker.internal:11434/api/tags
```

---

### Phase 2: Component Testing

**1. Test Engineering Plan Generator**
```bash
curl -X POST http://localhost:5678/webhook/planning-agent/engineering-plan \
  -H "Content-Type: application/json" \
  -d @sample_inputs/brds/tiny_test_brd.json
```

**Expected**:
- Response time: 20-30s
- Valid JSON engineering plan
- Quality check: All sections present

**2. Test Project Schedule Generator**
```bash
# Use a simplified engineering plan
curl -X POST http://localhost:5678/webhook/planning-agent/project-schedule \
  -H "Content-Type: application/json" \
  -d @tests/fixtures/simplified_engineering_plan.json
```

**Expected**:
- Response time: 15-25s
- Valid JSON schedule
- Dates in correct format

---

### Phase 3: End-to-End Testing

**1. Use test script**
```bash
./tests/integration/test_e2e_orchestrator.sh
```

**2. Use Streamlit UI**
- Load tiny_test_brd.json
- Process and verify outputs
- Check file generation

---

### Phase 4: Quality Comparison

**Create comparison test**:
```bash
# Run same BRD through both models
# Claude Haiku (v1.0.0)
git checkout main
./tests/integration/test_e2e_orchestrator.sh > claude_output.json

# Gemma 2 (new branch)
git checkout brd-agent-gemma-2
./tests/integration/test_e2e_orchestrator.sh > gemma_output.json

# Manual comparison
diff claude_output.json gemma_output.json
```

**Quality Metrics to Check**:
- ✅ All required JSON fields present
- ✅ Technical requirements are specific (not generic)
- ✅ Dates are realistic and consistent
- ✅ Dependencies are logical
- ✅ No hallucinated technologies
- ✅ JSON is valid (no parsing errors)

---

## 📊 Performance Expectations

### Baseline (Claude Haiku v1.0.0):
| Metric | Value |
|--------|-------|
| Engineering Plan | 15-20s |
| Project Schedule | 10-15s |
| Total Pipeline | 28-50s |
| Quality | 100% (reference) |
| Cost | $0.017/run |

### Target (Gemma 2 9B):
| Metric | Expected | Acceptable Range |
|--------|----------|------------------|
| Engineering Plan | 25-35s | 20-45s |
| Project Schedule | 20-30s | 15-40s |
| Total Pipeline | 60-90s | 45-120s |
| Quality | 80-85% | 75-90% |
| Cost | $0.00/run | $0.00/run |

### Memory Usage:
| Component | RAM |
|-----------|-----|
| macOS | 4GB |
| Docker (n8n + parser) | 3GB |
| Ollama + Gemma 2 9B | 9-10GB |
| **Total** | **16-17GB** |

**Note**: On 16GB Mac, expect occasional swap usage during peak load.

---

## 🔄 Rollback Plan

If Gemma 2 doesn't meet quality expectations:

### Quick Rollback (5 minutes):
```bash
# Switch back to main branch
git checkout main

# Restart services (no code changes needed)
docker-compose restart

# Test with Claude
./tests/integration/test_e2e_orchestrator.sh
```

### Hybrid Approach:
Keep both options and switch via environment variable:

```yaml
# docker-compose.yml
environment:
  - LLM_PROVIDER=${LLM_PROVIDER:-anthropic}  # anthropic or ollama
  - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
  - OLLAMA_HOST=http://host.docker.internal:11434
```

Update workflows to check `LLM_PROVIDER` and route accordingly.

---

## 📝 Implementation Checklist

### Pre-Migration (Setup):
- [ ] Install Ollama on macOS
- [ ] Pull Gemma 2 9B model
- [ ] Verify Ollama API accessibility
- [ ] Test basic model responses
- [ ] Backup current n8n workflows

### Engineering Plan Generator:
- [ ] Simplify prompt schema
- [ ] Reduce instruction verbosity
- [ ] Update HTTP Request node URL
- [ ] Update response parsing logic
- [ ] Test with tiny BRD
- [ ] Test with full BRD
- [ ] Compare output quality

### Project Schedule Generator:
- [ ] Create "Summarize Engineering Plan" node
- [ ] Update "Prepare AI Prompt" node
- [ ] Simplify schedule prompt
- [ ] Update HTTP Request node URL
- [ ] Update response parsing logic
- [ ] Test with simplified plan
- [ ] Test with full plan
- [ ] Compare output quality

### BRD Parser (Optional):
- [ ] Update Python dependencies
- [ ] Switch to OpenAI client
- [ ] Update API calls
- [ ] Test PDF parsing
- [ ] Test JSON extraction

### End-to-End Testing:
- [ ] Run integration test script
- [ ] Test via Streamlit UI
- [ ] Verify file outputs
- [ ] Compare with Claude outputs
- [ ] Measure performance
- [ ] Document quality differences

### Documentation:
- [ ] Update README.md (add Ollama setup)
- [ ] Update SETUP.md (add Gemma instructions)
- [ ] Update ARCHITECTURE.md (reflect new setup)
- [ ] Add GEMMA_TROUBLESHOOTING.md

---

## 🐛 Common Issues & Troubleshooting

### Issue 1: "Connection refused to localhost:11434"
**Cause**: Ollama not running or not accessible from Docker

**Fix**:
```bash
# Check Ollama is running
ps aux | grep ollama

# Start Ollama if needed
ollama serve

# Test from Docker container
docker exec -it brd_agent_em_n8n_1 curl http://host.docker.internal:11434/api/tags
```

---

### Issue 2: "Model not found: gemma2:9b"
**Cause**: Model not pulled or wrong name

**Fix**:
```bash
# List available models
ollama list

# Pull the model
ollama pull gemma2:9b

# Verify
ollama run gemma2:9b "test"
```

---

### Issue 3: Slow performance (>2 minutes)
**Cause**: High memory pressure, swapping to disk

**Fix**:
```bash
# Close other applications
# Check memory usage
top -o MEM

# Consider using smaller model
ollama pull gemma2:2b  # Uses only 3-4GB RAM
```

---

### Issue 4: Poor quality output
**Symptoms**: Generic responses, missing details, incorrect JSON

**Fix**:
1. **Increase temperature** (0.7 → 0.8 for more creativity)
2. **Add examples** to prompts (show desired output format)
3. **Add validation** and retry logic
4. **Try different quantization**: `gemma2:9b-q8` (higher quality)

---

### Issue 5: JSON parsing errors
**Cause**: Model outputs markdown formatting or extra text

**Fix**:
```javascript
// Enhanced cleaning in Format Output node
let aiResponse = response.choices?.[0]?.message?.content || '';

// Remove markdown
aiResponse = aiResponse.replace(/```json\n?/g, '').replace(/```\n?/g, '');

// Remove any text before first {
const jsonStart = aiResponse.indexOf('{');
if (jsonStart > 0) {
  aiResponse = aiResponse.substring(jsonStart);
}

// Remove any text after last }
const jsonEnd = aiResponse.lastIndexOf('}');
if (jsonEnd > 0 && jsonEnd < aiResponse.length - 1) {
  aiResponse = aiResponse.substring(0, jsonEnd + 1);
}

aiResponse = aiResponse.trim();
```

---

### Issue 6: Context length exceeded
**Error**: "Context length 8500 exceeds maximum 8192"

**Fix**:
1. Further reduce prompt verbosity
2. Compress BRD input more aggressively
3. Use multi-step approach (generate in chunks)

---

## 💰 Cost-Benefit Analysis

### One-Time Costs:
| Item | Effort | Value |
|------|--------|-------|
| Setup Ollama | 30 min | Easy |
| Prompt optimization | 4-8 hours | Moderate |
| Workflow updates | 2-4 hours | Easy |
| Testing & validation | 4-6 hours | Moderate |
| Documentation | 2-3 hours | Easy |
| **Total** | **12-21 hours** | **Medium effort** |

### Ongoing Benefits:
| Factor | Claude Haiku | Gemma 2 9B | Savings |
|--------|--------------|------------|---------|
| Cost/run | $0.017 | $0.00 | 100% |
| Cost/1000 runs | $17 | $0 | $17 |
| Cost/10000 runs | $170 | $0 | $170 |
| **Annual (1000 runs)** | **$204** | **$0** | **$204** |

### Break-even Point:
- **Low usage** (<500 runs/year): Not worth it
- **Medium usage** (500-5000 runs/year): Depends on quality needs
- **High usage** (>5000 runs/year): Definitely worth it
- **Experimentation/Learning**: Priceless 🎓

---

## 🎯 Recommendation

### When to Migrate:
✅ **Good reasons**:
- Learning/experimentation with local LLMs
- Privacy requirements (no data leaves your machine)
- High usage volume (>1000 runs/year)
- Want to eliminate API dependencies
- Have time for optimization (12-21 hours)

❌ **Avoid if**:
- Need highest quality (Claude still better)
- Low usage volume (<500 runs/year)
- Time-constrained (fast responses critical)
- Limited hardware (8GB RAM or less)
- Don't want to maintain local infrastructure

### Hybrid Approach (Best of Both):
Keep both options and switch based on use case:
- **Development**: Gemma 2 (free, fast iteration)
- **Production**: Claude (quality, reliability)
- **Sensitive data**: Gemma 2 (privacy)
- **Critical projects**: Claude (quality)

---

## 📚 Additional Resources

### Ollama Documentation:
- Official site: https://ollama.com
- Model library: https://ollama.com/library
- API docs: https://github.com/ollama/ollama/blob/main/docs/api.md

### Gemma 2 Information:
- Model card: https://huggingface.co/google/gemma-2-9b
- Technical report: https://ai.google.dev/gemma
- Best practices: https://github.com/google/gemma_pytorch

### Prompt Engineering:
- Gemma prompt guide: https://ai.google.dev/gemma/docs/formatting
- Few-shot examples: https://ai.google.dev/gemma/docs/prompting
- JSON generation tips: https://cookbook.openai.com/examples/how_to_format_inputs_to_chatgpt_models

---

## 📞 Support & Questions

For migration support:
1. Check troubleshooting section above
2. Review Ollama logs: `ollama logs`
3. Test model directly: `ollama run gemma2:9b`
4. Check n8n execution logs in UI
5. Verify Docker networking: `docker exec -it <container> curl http://host.docker.internal:11434/api/tags`

---

## 🏁 Final Notes

This migration is **optional** and can be done incrementally:
1. Start with Engineering Plan Generator only
2. Test quality thoroughly
3. If satisfied, migrate Schedule Generator
4. Keep Claude as fallback

The current v1.0.0 with Claude Haiku is **production-ready and works well**. This migration is for:
- Cost optimization (high usage scenarios)
- Privacy requirements
- Learning and experimentation
- Eliminating external dependencies

**Take your time, test thoroughly, and don't hesitate to stick with Claude if Gemma doesn't meet your quality bar.** 🎯

---

*Document Version: 1.0*  
*Last Updated: November 23, 2025*  
*Target Branch: `brd-agent-gemma-2`*

