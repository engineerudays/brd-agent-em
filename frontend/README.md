# 🎨 BRD Agent - Frontend UI

Streamlit-based web interface for the BRD Agent Multi-Agent Engineering Manager.

---

## ✨ Features

- **📝 BRD Input** - Upload JSON files or paste directly
- **🔄 Real-time Processing** - Submit to orchestrator and track status
- **📊 Results Display** - View generated engineering plans and schedules
- **📅 Timeline Visualization** - Project timeline and milestones
- **💾 Download Outputs** - Export generated artifacts
- **🎨 Modern UI** - Clean, intuitive interface

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Running BRD Agent backend (Docker Compose)

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
pip install -r requirements.txt

# Or use a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the App

```bash
# From the frontend directory
streamlit run app.py

# Or from project root
streamlit run frontend/app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## 📖 Usage Guide

### Step 1: Input BRD

Choose one of three methods:

1. **Upload JSON File**
   - Click "Browse files"
   - Select your BRD JSON file

2. **Paste JSON**
   - Copy your BRD JSON
   - Paste into the text area

3. **Load Sample**
   - Click "Load Sample" to use the demo BRD

### Step 2: Process

1. Verify the BRD preview shows ✅ Valid
2. Click **🚀 Process BRD** button
3. Wait for processing (typically 30-60 seconds)

### Step 3: View Results

Navigate through tabs:
- **📊 Results** - Processing summary and status
- **📅 Timeline** - Project schedule information

### Step 4: Download

Click **💾 Download** to save the full response

---

## ⚙️ Configuration

### Orchestrator URL

Default: `http://localhost:5678/webhook/orchestrator/process-brd-v2`

To change:
1. Click sidebar **⚙️ Configuration**
2. Update **Orchestrator URL** field

### Environment Variables

Create `.env` file in `frontend/` directory:

```bash
ORCHESTRATOR_URL=http://localhost:5678/webhook/orchestrator/process-brd-v2
```

---

## 🎯 BRD Format

### Required Structure

```json
{
  "project": {
    "name": "Your Project Name",
    "description": "Brief description",
    "objectives": ["Objective 1", "Objective 2"]
  },
  "features": [
    {
      "id": "F001",
      "name": "Feature Name",
      "description": "Feature description",
      "priority": "High"
    }
  ],
  "stakeholders": ["Stakeholder 1"],
  "technical_requirements": {
    "platforms": ["Web", "Mobile"],
    "performance": "Requirements",
    "security": "Requirements"
  }
}
```

### Sample BRD

See `sample_inputs/brds/brd_input_cleaner.json` for a complete example.

---

## 🛠️ Development

### Project Structure

```
frontend/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration settings
├── utils.py              # Utility functions (API, charts)
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

### Adding Features

1. **New utility function**: Add to `utils.py`
2. **New configuration**: Add to `config.py`
3. **New UI component**: Add to `app.py`

### Running in Development Mode

```bash
# Enable auto-reload on file changes
streamlit run app.py --server.runOnSave true

# Run on different port
streamlit run app.py --server.port 8502
```

---

## 🐛 Troubleshooting

### "Connection refused" Error

**Problem**: Cannot connect to orchestrator

**Solution**:
1. Verify backend is running: `docker-compose ps`
2. Check orchestrator URL in sidebar
3. Ensure n8n workflows are activated

### "Invalid JSON" Error

**Problem**: BRD JSON is malformed

**Solution**:
1. Validate JSON using online validator
2. Check for missing commas or brackets
3. Use sample BRD as template

### Slow Processing

**Problem**: Processing takes > 2 minutes

**Solution**:
1. Check Docker logs: `docker-compose logs -f`
2. Verify Anthropic API key is configured
3. Check n8n workflow execution logs

---

## 📊 Features Detail

### Tabs Overview

| Tab | Features |
|-----|----------|
| **Input & Process** | File upload, JSON paste, sample loader, validation, submit button |
| **Results** | Processing summary, status metrics, stage completion, full response, download |
| **Timeline** | Timeline information, output directory reference |

### Sidebar

- **Configuration**: Orchestrator URL settings
- **Quick Stats**: Agent count, output types
- **Help**: Usage guide, templates

---

## 🚀 Deployment

### Production Deployment

For production deployment, consider:

1. **Use HTTPS** for orchestrator URL
2. **Set environment variables** properly
3. **Use process manager** like PM2 or systemd
4. **Configure firewall** rules

### Docker Deployment (Future)

```dockerfile
# Dockerfile example
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## 📝 Future Enhancements

- [ ] Enhanced Gantt chart visualization
- [ ] Real-time status polling
- [ ] History of processed BRDs
- [ ] PDF export functionality
- [ ] Side-by-side comparison
- [ ] Authentication & user management
- [ ] Dark mode theme

---

## 🤝 Contributing

This is part of the BRD Agent project. See main README for contribution guidelines.

---

## 📄 License

MIT License - See main project LICENSE file.

---

## 🆘 Support

For issues related to the frontend:
1. Check this README
2. Review Streamlit logs in terminal
3. Check browser console for errors
4. Verify backend is running properly

For backend issues, see main project [SETUP.md](../SETUP.md)

---

**Built with ❤️ using Streamlit, Plotly, and Python**

