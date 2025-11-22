"""
Utility functions for BRD Agent UI
"""
import json
import requests
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional


def submit_brd_to_orchestrator(brd_data: Dict[str, Any], orchestrator_url: str) -> Dict[str, Any]:
    """
    Submit BRD to the orchestrator API.
    
    Args:
        brd_data: BRD data as dictionary
        orchestrator_url: Orchestrator endpoint URL
        
    Returns:
        Response from orchestrator
    """
    try:
        response = requests.post(
            orchestrator_url,
            json={"body": brd_data},
            headers={"Content-Type": "application/json"},
            timeout=180  # 3 minutes timeout
        )
        response.raise_for_status()
        
        # Check if response has content
        if not response.content:
            return {
                "success": False,
                "error": "Empty response from orchestrator. Check if the workflow is activated in n8n.",
                "status_code": response.status_code,
                "debug_info": f"URL: {orchestrator_url}"
            }
        
        # Try to parse JSON
        try:
            json_data = response.json()
            return {
                "success": True,
                "data": json_data,
                "status_code": response.status_code
            }
        except json.JSONDecodeError as je:
            return {
                "success": False,
                "error": f"Invalid JSON response: {str(je)}",
                "status_code": response.status_code,
                "debug_info": f"Response preview: {response.text[:500]}"
            }
            
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timed out. The orchestrator may be processing a large BRD.",
            "status_code": 0
        }
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        debug_info = ""
        
        if hasattr(e, 'response') and e.response is not None:
            try:
                debug_info = f"Response: {e.response.text[:500]}"
            except:
                debug_info = "Could not read response text"
        
        return {
            "success": False,
            "error": error_msg,
            "status_code": getattr(e.response, 'status_code', 0) if hasattr(e, 'response') else 0,
            "debug_info": debug_info
        }


def validate_brd_json(brd_text: str) -> tuple[bool, Optional[Dict], Optional[str]]:
    """
    Validate BRD JSON format.
    Accepts multiple formats:
    1. Direct BRD: {project: {...}, features: [...]}
    2. Parser format: {raw_brd_text: "..."}
    3. Wrapped format: {brd_data: {...}}
    
    Returns:
        (is_valid, parsed_json, error_message)
    """
    try:
        data = json.loads(brd_text)
        
        # Basic validation
        if not isinstance(data, dict):
            return False, None, "BRD must be a JSON object"
        
        # Accept multiple BRD formats
        # Format 1: Direct BRD with project/features
        if "project" in data or "features" in data:
            return True, data, None
        
        # Format 2: Parser format with raw_brd_text
        if "raw_brd_text" in data:
            return True, data, None
        
        # Format 3: Wrapped in brd_data
        if "brd_data" in data:
            return True, data, None
        
        # If none of the expected formats, show helpful error
        return False, None, "BRD must contain one of: 'project', 'features', 'raw_brd_text', or 'brd_data'"
            
    except json.JSONDecodeError as e:
        return False, None, f"Invalid JSON: {str(e)}"


def create_gantt_chart(schedule_data: Dict[str, Any]) -> Optional[go.Figure]:
    """
    Create a Gantt chart from project schedule data.
    
    Args:
        schedule_data: Project schedule with phases and tasks
        
    Returns:
        Plotly figure or None if data is invalid
    """
    try:
        project_schedule = schedule_data.get("project_schedule", {})
        phases = project_schedule.get("phases", [])
        
        if not phases:
            return None
            
        # Prepare data for Gantt chart
        tasks = []
        
        for phase in phases:
            phase_name = phase.get("phase_name", "Unnamed Phase")
            start_date = phase.get("start_date", "2025-01-01")
            end_date = phase.get("end_date", "2025-01-01")
            
            # Add phase as a task
            tasks.append({
                "Task": phase_name,
                "Start": start_date,
                "Finish": end_date,
                "Type": "Phase"
            })
            
            # Add milestones
            for milestone in phase.get("milestones", []):
                milestone_name = milestone.get("name", "Unnamed Milestone")
                target_date = milestone.get("target_date", start_date)
                
                tasks.append({
                    "Task": f"  📍 {milestone_name}",
                    "Start": target_date,
                    "Finish": target_date,
                    "Type": "Milestone"
                })
        
        if not tasks:
            return None
            
        # Create DataFrame
        df = pd.DataFrame(tasks)
        
        # Create Gantt chart
        fig = px.timeline(
            df,
            x_start="Start",
            x_end="Finish",
            y="Task",
            color="Type",
            title="Project Timeline",
            color_discrete_map={"Phase": "#0066cc", "Milestone": "#28a745"}
        )
        
        fig.update_layout(
            xaxis_title="Timeline",
            yaxis_title="Tasks",
            height=400 + len(tasks) * 30,  # Dynamic height
            showlegend=True,
            hovermode="closest"
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating Gantt chart: {e}")
        return None


def format_duration(weeks: int) -> str:
    """Format duration in weeks to human-readable format."""
    if weeks < 4:
        return f"{weeks} weeks"
    elif weeks < 52:
        months = round(weeks / 4.33, 1)
        return f"{months} months"
    else:
        years = round(weeks / 52, 1)
        return f"{years} years"


def extract_project_summary(response_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract key metrics from orchestrator response for summary display.
    
    Returns:
        Dictionary with summary metrics
    """
    summary = {
        "status": "Unknown",
        "stages_completed": [],
        "timestamp": None
    }
    
    try:
        summary["status"] = response_data.get("status", "Unknown")
        summary["stages_completed"] = response_data.get("stages_completed", [])
        summary["timestamp"] = response_data.get("timestamp")
        
        return summary
        
    except Exception as e:
        print(f"Error extracting summary: {e}")
        return summary


def get_sample_brds() -> Dict[str, str]:
    """
    Get available sample BRDs.
    
    Returns:
        Dictionary mapping BRD name to file path
    """
    import os
    from pathlib import Path
    
    samples = {}
    sample_dir = Path(__file__).parent / "sample_brds"
    
    if sample_dir.exists():
        for file_path in sample_dir.glob("*.json"):
            samples[file_path.stem.replace("_", " ").title()] = str(file_path)
    
    return samples


def load_sample_brd(file_path: str) -> Optional[str]:
    """Load a sample BRD file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return json.dumps(data, indent=2)
    except Exception as e:
        print(f"Error loading sample BRD: {e}")
        return None

