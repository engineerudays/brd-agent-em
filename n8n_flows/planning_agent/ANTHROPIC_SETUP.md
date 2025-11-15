# Anthropic API Setup Guide for n8n

These workflows use the **HTTP Request node** with Anthropic's API directly, which works with any version of n8n.

## 📝 Step-by-Step Setup

### 1. Get Your Anthropic API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to **API Keys** section
4. Click **Create Key**
5. Give it a name (e.g., "n8n Planning Agent")
6. **Copy the API key** (you won't be able to see it again!)

### 2. Add Credentials to n8n

1. In n8n, click the **🔑 icon** in the left sidebar (or go to **Settings** → **Credentials**)
2. Click **Add Credential**
3. Search for **"Header Auth"** or **"HTTP Header Auth"**
4. Fill in the details:
   - **Credential Name**: `Anthropic Header Auth` (or any name you prefer)
   - **Name**: `x-api-key`
   - **Value**: Paste your Anthropic API key (starts with `sk-ant-...`)
5. Click **Save**

### 3. Import the Workflows

1. Go to **Workflows** in n8n
2. Click **Add Workflow** → **Import from File**
3. Import both files:
   - `engineering_plan/structured_plan_generator.json`
   - `project_schedule/project_schedule_generator.json`

### 4. Link Credentials to Workflows

For each imported workflow:

1. Open the workflow
2. Click on the **"AI - Generate..."** node (the HTTP Request node)
3. In the node settings, find **Authentication** section
4. Select **Header Auth**
5. Choose your saved credential: **"Anthropic Header Auth"**
6. Click **Execute Node** to test (should work if credentials are correct)

### 5. Activate Workflows

1. Toggle **Active** switch in the top-right corner
2. Note the webhook URLs displayed
3. You're ready to use the workflows!

## 🧪 Testing Your Setup

### Test the Engineering Plan Generator

```bash
curl -X POST http://localhost:5678/webhook-test/planning-agent/engineering-plan \
  -H "Content-Type: application/json" \
  -d '{
    "raw_brd_text": "{\"document_info\":{\"title\":\"Test Project\"},\"business_objectives\":[{\"objective\":\"Test\"}],\"requirements\":{\"functional\":[],\"non_functional\":[]}}"
  }'
```

**Note:** Replace `localhost:5678` with your n8n URL. Also, n8n appends `/webhook-test/` for test mode URLs.

### Test in Production Mode

Once you activate the workflow, use the production webhook URL (without `/webhook-test/`):

```bash
curl -X POST http://localhost:5678/webhook/planning-agent/engineering-plan \
  -H "Content-Type: application/json" \
  -d '{
    "raw_brd_text": "{\"document_info\":{\"title\":\"Test Project\"},\"business_objectives\":[{\"objective\":\"Test\"}],\"requirements\":{\"functional\":[],\"non_functional\":[]}}"
  }'
```

## 🔍 Troubleshooting

### Error: "401 Unauthorized"
- **Cause**: Invalid API key
- **Solution**: Double-check your Anthropic API key. Make sure you copied it correctly with no extra spaces.

### Error: "Missing authentication"
- **Cause**: Credentials not linked to the HTTP Request node
- **Solution**: 
  1. Open the workflow
  2. Click the "AI - Generate..." node
  3. Under **Credentials**, select your Header Auth credential
  4. Save the workflow

### Error: "Could not find credential"
- **Cause**: The credential name in the JSON doesn't match your actual credential
- **Solution**: 
  1. Open the HTTP Request node
  2. Clear the existing credential selection
  3. Manually select your credential from the dropdown
  4. Save

### Workflow not triggering
- **Cause**: Workflow might not be activated
- **Solution**: Make sure the **Active** toggle is ON (top-right corner)

### JSON parsing error in response
- **Cause**: Claude sometimes adds markdown formatting
- **Solution**: The workflow has built-in cleanup, but if issues persist:
  1. Check the **Format...Output** node
  2. Look at the raw AI response
  3. Adjust the markdown cleanup regex if needed

## 💡 Understanding the HTTP Request Approach

### Why use HTTP Request instead of a dedicated node?

1. **Universal Compatibility**: Works with any n8n version (Docker, npm, cloud)
2. **No Dependencies**: Doesn't require installing community nodes
3. **Full Control**: You can customize the API request exactly as needed
4. **Easy Debugging**: Can see and modify the exact API call being made

### The Request Structure

The HTTP Request node calls Anthropic's Messages API:

```json
{
  "model": "claude-3-5-sonnet-20240620",
  "max_tokens": 4000,
  "temperature": 0.7,
  "messages": [
    {
      "role": "user",
      "content": "Your prompt here..."
    }
  ]
}
```

### Available Claude Models

If you encounter model errors, you can change the model in the HTTP Request node. Available models:

- **`claude-3-haiku-20240307`** ✅ **(Default - Most Compatible)**
  - Fastest and most cost-effective
  - Widely available across all regions
  - Excellent for structured planning tasks
  - $0.25 input / $1.25 output per million tokens
  
- **`claude-3-5-sonnet-20240620`**
  - Best balance of intelligence, speed, and cost
  - May require specific API access
  - Excellent for complex technical tasks

- **`claude-3-sonnet-20240229`**
  - Good performance, moderate cost
  - May not be available in all regions

- **`claude-3-opus-20240229`**
  - Most capable model
  - Highest cost ($15 input / $75 output per million tokens)
  - May require upgraded API access

To change the model:
1. Open the workflow
2. Click **"AI - Generate..."** node
3. Edit the **JSON Body**
4. Change the `"model"` value
5. Save and test

With the header:
```
x-api-key: sk-ant-your-key-here
anthropic-version: 2023-06-01
```

## 📊 API Costs

**Claude 3.5 Sonnet Pricing:**
- Input: $3 per million tokens (~$0.003 per 1,000 tokens)
- Output: $15 per million tokens (~$0.015 per 1,000 tokens)

**Estimated costs for typical BRD:**
- Engineering Plan generation: ~$0.10 - $0.30 per request
- Project Schedule generation: ~$0.15 - $0.35 per request

Much cheaper than hiring a project manager! 😄

## 🔐 Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** in production
3. **Rotate keys** periodically
4. **Monitor usage** in Anthropic console
5. **Set spending limits** in Anthropic account settings

## 📚 Additional Resources

- [Anthropic API Documentation](https://docs.anthropic.com/en/api/getting-started)
- [Claude Models Overview](https://docs.anthropic.com/en/docs/models-overview)
- [n8n HTTP Request Node Docs](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/)
- [n8n Credentials Guide](https://docs.n8n.io/credentials/)

## ✅ Quick Checklist

Before using the workflows, make sure:

- [ ] Anthropic account created
- [ ] API key generated and copied
- [ ] Header Auth credential created in n8n
- [ ] Credential name is `x-api-key` (header name)
- [ ] API key pasted as the value
- [ ] Both workflows imported
- [ ] Credentials linked to HTTP Request nodes
- [ ] Workflows activated
- [ ] Test request sent successfully

---

**Having issues?** Check the n8n execution logs (click on a workflow execution to see detailed logs of each node).

