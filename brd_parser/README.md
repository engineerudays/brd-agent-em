# BRD Parser Module

This module handles the parsing and processing of Business Requirements Documents (BRDs).

## 🏗️ Architecture

The BRD Parser consists of two components:

1. **Python FastAPI Service** (`main.py`) - PDF processing and AI extraction
2. **n8n Integration Workflow** (`brd_input_cleaner.json`) - n8n webhook integration

## 📁 Structure

```
brd_parser/
├── main.py                 # FastAPI service
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker image
├── ENV_TEMPLATE.md        # Environment variables template
├── brd_input_cleaner.json # n8n workflow (to be created)
├── workflows/             # Additional workflow files
├── schemas/               # JSON schemas
└── utils/                 # Helper scripts
```

## 🚀 Setup

### 1. Environment Configuration

Create a `.env` file in the `brd_parser/` directory:

```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

See `ENV_TEMPLATE.md` for details.

### 2. Docker Deployment (Recommended)

```bash
# From project root
cd /Users/udayammanagi/Udays-Folder/IK/brd_agent_em

# Start all services (n8n + BRD Parser)
docker-compose up -d

# Check services
docker-compose ps

# View logs
docker-compose logs -f brd-parser
```

### 3. Local Development (Optional)

```bash
cd brd_parser

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run service
python main.py

# Service will be available at http://localhost:8000
```

## 🔌 API Endpoints

### Health Check
```bash
GET http://localhost:8000/health
```

### Parse PDF BRD
```bash
POST http://localhost:8000/parse/pdf
Content-Type: multipart/form-data

# Body: file upload (PDF)
```

Example with curl:
```bash
curl -X POST http://localhost:8000/parse/pdf \
  -F "file=@path/to/your/brd.pdf"
```

### Parse Text BRD
```bash
POST http://localhost:8000/parse/text
Content-Type: application/json

{
  "text": "Your BRD text content here..."
}
```

## 📊 Output Format

The parser returns structured JSON compatible with the Engineering Plan Generator:

```json
{
  "status": "success",
  "message": "BRD parsed successfully",
  "data": {
    "project": {
      "name": "Customer Onboarding Portal",
      "description": "...",
      "objectives": ["..."],
      "constraints": ["..."]
    },
    "features": [
      {
        "id": "F001",
        "name": "User Registration",
        "description": "...",
        "priority": "High",
        "requirements": ["..."]
      }
    ],
    "stakeholders": ["Product Team", "Engineering", "..."],
    "technical_requirements": {
      "platforms": ["Web", "Mobile"],
      "integrations": ["..."],
      "performance": "...",
      "security": "...",
      "scalability": "..."
    },
    "success_criteria": ["..."]
  },
  "metadata": {
    "filename": "brd.pdf",
    "text_length": 5432,
    "features_count": 5
  }
}
```

## 🧪 Testing

### Test with Sample PDF

```bash
# Upload a PDF BRD
curl -X POST http://localhost:8000/parse/pdf \
  -F "file=@sample_inputs/brds/sample_brd.pdf" \
  | jq '.'
```

### Test with Text

```bash
curl -X POST http://localhost:8000/parse/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Project: E-commerce Platform. Features: User authentication, Product catalog, Shopping cart..."}' \
  | jq '.'
```

## 🔗 Integration with n8n

The `brd_input_cleaner.json` workflow will:

1. **Webhook Trigger** - Receive BRD upload request
2. **Call Parser Service** - HTTP Request to `http://brd-parser:8000/parse/pdf`
3. **Validate Response** - Check if parsing succeeded
4. **Extract Data** - Pull the structured data from response
5. **Pass to Next Agent** - Send to Engineering Plan Generator or store for later

## 🐳 Docker Network

The BRD Parser service runs on the same Docker network as n8n:

- **Service name**: `brd-parser` (use this in n8n HTTP Request nodes)
- **Internal URL**: `http://brd-parser:8000`
- **External URL**: `http://localhost:8000`

## ❌ Troubleshooting

### Service won't start

```bash
# Check logs
docker-compose logs brd-parser

# Common issues:
# - Missing .env file with ANTHROPIC_API_KEY
# - Port 8000 already in use
# - Invalid API key
```

### PDF parsing fails

- Ensure PDF is text-based (not scanned image)
- Check file size (large PDFs may timeout)
- Verify PDF is not encrypted/password-protected

### AI extraction returns errors

- Verify ANTHROPIC_API_KEY is valid
- Check API quota/billing status
- Review logs for specific error messages

## 📝 Main Workflow File

⚠️ **Important Submission Requirement:**

The primary BRD parser workflow should be placed directly in this directory:
- **`brd_input_cleaner.json`** - Exported from n8n BRD Input Parser flow

## 🎯 Purpose

- Parse incoming BRD documents (PDF/Text)
- Clean and validate BRD input
- Extract key information using AI
- Transform BRDs into structured data
- Route to appropriate agents (Planning or Design)

## 🔄 Integration with Multi-Agent System

The BRD Parser is the entry point for the entire system:
1. Receives raw BRD input (PDF/Text/JSON)
2. Extracts text from PDF if needed
3. Uses AI to structure the information
4. Validates and formats the output
5. Routes to Planning Agent or Design Agent

