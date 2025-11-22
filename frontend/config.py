"""
Configuration settings for BRD Agent UI
"""
import os

# API Configuration
ORCHESTRATOR_URL = os.getenv(
    "ORCHESTRATOR_URL", 
    "http://localhost:5678/webhook/orchestrator/process-brd-v2"
)

# UI Configuration
APP_TITLE = "🤖 BRD Agent - Engineering Manager"
APP_ICON = "🤖"
PAGE_LAYOUT = "wide"

# Sample BRDs directory
SAMPLE_BRDS_DIR = "sample_brds"

# Color scheme
COLORS = {
    "primary": "#0066cc",
    "success": "#28a745",
    "danger": "#dc3545",
    "warning": "#ffc107",
    "info": "#17a2b8",
}

# Feature status colors for roadmap
STATUS_COLORS = {
    "completed": "#28a745",
    "in_progress": "#ffc107",
    "planned": "#6c757d",
}

