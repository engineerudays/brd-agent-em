# Setup Instructions for Dual-Format Output (JSON + TXT)

## 🎯 Goal
Generate BOTH a clean JSON file AND a human-readable TXT file for each engineering plan.

## 📋 Steps to Implement in n8n

### Step 1: Update the JSON Generation (Already Done!)
Your current "Prepare File Data" node should already be generating clean JSON. ✅

### Step 2: Add TXT Generation Branch

1. **In n8n, open your workflow**

2. **Add a NEW Code node:**
   - Click on the canvas
   - Search for "Code"
   - Add a "Code" node
   - Name it: **"Prepare TXT File Data"**

3. **Position it:**
   - Place it parallel to (next to) the "Prepare File Data" node
   - Both should be connected FROM "Format Engineering Plan Output"

4. **Copy the TXT generation code:**
   - Open: `n8n_flows/planning_agent/engineering_plan/TXT_FILE_NODE.js`
   - Copy ALL the code
   - Paste into the new "Prepare TXT File Data" node

5. **Add another Write Binary File node:**
   - Add a "Write Binary File" node
   - Name it: **"Write TXT File"**
   - Connect: "Prepare TXT File Data" → "Write TXT File"
   - Set fileName: `={{$json.filepath}}`

### Step 3: Update Workflow Connections

Your workflow should now look like this:

```
Format Engineering Plan Output
        ↓ (splits into 3 branches)
        ├─→ Save to State
        ├─→ Prepare File Data → Write File to Disk (JSON)
        └─→ Prepare TXT File Data → Write TXT File (TXT)
                                            ↓
                                    Respond with Plan
```

### Step 4: Save and Test

1. **Save the workflow**
2. **Run the test:**

```bash
cd /Users/udayammanagi/Udays-Folder/IK/brd_agent_em

curl -X POST http://localhost:5678/webhook/planning-agent/engineering-plan \
  -H "Content-Type: application/json" \
  -d @sample_inputs/brds/brd_input_cleaner.json
```

3. **Check outputs:**

```bash
ls -la sample_inputs/outputs/engineering_plans/
```

You should see TWO new files with the same timestamp:
- `engineering_plan_customer_onboarding_..._v1_2025-11-15T15-XX-XX.json`
- `engineering_plan_customer_onboarding_..._v1_2025-11-15T15-XX-XX.txt`

## ✅ Verification

Open the TXT file:
```bash
cat sample_inputs/outputs/engineering_plans/*.txt | head -50
```

You should see the beautiful formatted report with boxes, emojis, and sections!

## 🐛 Troubleshooting

**If TXT file is not created:**
1. Check that "Prepare TXT File Data" node is connected properly
2. Verify the "Write TXT File" node has fileName: `={{$json.filepath}}`
3. Check n8n execution logs for errors

**If both nodes conflict:**
- Make sure they're both connected FROM "Format Engineering Plan Output"
- NOT connected to each other sequentially

## 📸 Visual Guide

```
┌─────────────────────────────────┐
│ Format Engineering Plan Output  │
└────────────┬────────────────────┘
             │
      ┌──────┴──────┬─────────────┐
      │             │             │
      ▼             ▼             ▼
┌─────────┐  ┌────────────┐  ┌────────────────┐
│  Save   │  │  Prepare   │  │   Prepare TXT  │
│  State  │  │  File Data │  │   File Data    │
└─────────┘  └─────┬──────┘  └───────┬────────┘
                   │                 │
                   ▼                 ▼
            ┌─────────────┐   ┌──────────────┐
            │ Write File  │   │ Write TXT    │
            │   (JSON)    │   │   File       │
            └──────┬──────┘   └──────┬───────┘
                   │                 │
                   └────────┬────────┘
                            │
                            ▼
                   ┌────────────────┐
                   │    Respond     │
                   └────────────────┘
```

---

**Need help?** Check the n8n execution logs or let me know!

