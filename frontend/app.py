"""
BRD Agent - Streamlit UI
Multi-Agent Engineering Manager Interface
"""
import streamlit as st
import json
from pathlib import Path
import sys

# Add parent directory to path to import from project root
sys.path.append(str(Path(__file__).parent.parent))

from frontend import config, utils

# Page configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout=config.PAGE_LAYOUT,
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0066cc;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        border-left: 4px solid #0066cc;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)


def render_header():
    """Render the main header"""
    st.markdown('<div class="main-header">🤖 BRD Agent - Engineering Manager</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Transform Business Requirements into Engineering Artifacts with AI</div>', unsafe_allow_html=True)
    st.divider()


def render_sidebar():
    """Render the sidebar with configuration and help"""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Orchestrator URL
        orchestrator_url = st.text_input(
            "Orchestrator URL",
            value=config.ORCHESTRATOR_URL,
            help="n8n Master Orchestrator webhook endpoint"
        )
        
        st.divider()
        
        # Quick stats
        st.header("📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Agents", "3")
        with col2:
            st.metric("Outputs", "2")
        
        st.caption("✅ Engineering Plan")
        st.caption("✅ Project Schedule")
        st.caption("🚧 Architecture (Coming Soon)")
        
        st.divider()
        
        # Help section
        st.header("❓ Help")
        with st.expander("How to Use"):
            st.markdown("""
            1. **Upload or paste** your BRD in JSON format
            2. **Click Process** to submit to the orchestrator
            3. **View results** with visual timeline
            4. **Download** generated artifacts
            
            **Required BRD Structure:**
            ```json
            {
              "project": {
                "name": "...",
                "description": "...",
                "objectives": [...]
              },
              "features": [...]
            }
            ```
            """)
        
        with st.expander("Sample Templates"):
            st.markdown("""
            Use the **Sample BRDs** tab to load
            pre-configured templates for testing.
            """)
        
        return orchestrator_url


def render_input_tab():
    """Render the BRD input tab"""
    st.header("📝 BRD Input")
    
    # Input method selection
    input_method = st.radio(
        "Input Method",
        ["Upload JSON File", "Paste JSON", "Load Sample"],
        horizontal=True
    )
    
    brd_text = None
    
    if input_method == "Upload JSON File":
        uploaded_file = st.file_uploader(
            "Upload BRD JSON file",
            type=["json"],
            help="Upload a Business Requirements Document in JSON format"
        )
        
        if uploaded_file:
            brd_text = uploaded_file.read().decode("utf-8")
            st.success(f"✅ Loaded: {uploaded_file.name}")
            
    elif input_method == "Paste JSON":
        brd_text = st.text_area(
            "Paste BRD JSON",
            height=300,
            placeholder='{\n  "project": {\n    "name": "Your Project",\n    ...\n  }\n}',
            help="Paste your BRD in JSON format"
        )
        
    else:  # Load Sample
        # Try to load sample from project's sample_inputs
        sample_path = Path(__file__).parent.parent / "sample_inputs" / "brds" / "brd_input_cleaner.json"
        
        if sample_path.exists():
            with open(sample_path, 'r') as f:
                sample_data = json.load(f)
                brd_text = json.dumps(sample_data, indent=2)
                
            st.info("📋 Sample BRD loaded: Customer Onboarding Portal")
        else:
            st.warning("Sample BRD not found. Please use Upload or Paste method.")
    
    # Display and validate BRD
    if brd_text:
        st.subheader("BRD Preview")
        
        # Validate
        is_valid, parsed_data, error = utils.validate_brd_json(brd_text)
        
        if is_valid:
            st.success("✅ Valid BRD JSON")
            
            # Show preview
            with st.expander("View BRD Details", expanded=False):
                st.json(parsed_data)
            
            # Store in session state
            st.session_state['brd_data'] = parsed_data
            st.session_state['brd_text'] = brd_text
            
            return True
        else:
            st.error(f"❌ Invalid BRD: {error}")
            st.code(brd_text, language="json")
            return False
    
    return False


def render_processing_section(orchestrator_url: str):
    """Render the processing section with submit button"""
    if 'brd_data' not in st.session_state:
        st.info("👆 Please provide a BRD in the input section above")
        return
    
    st.header("🚀 Process BRD")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.write("Ready to generate engineering artifacts from your BRD")
    
    with col2:
        if st.button("🚀 Process BRD", type="primary", use_container_width=True):
            process_brd(orchestrator_url)
    
    with col3:
        if st.button("🗑️ Clear", use_container_width=True):
            clear_session()


def process_brd(orchestrator_url: str):
    """Process the BRD through the orchestrator"""
    with st.spinner("⏳ Processing BRD through multi-agent pipeline..."):
        result = utils.submit_brd_to_orchestrator(
            st.session_state['brd_data'],
            orchestrator_url
        )
        
        if result['success']:
            st.session_state['result'] = result['data']
            st.session_state['processing_complete'] = True
            st.success("✅ BRD processed successfully!")
            st.rerun()
        else:
            st.error(f"❌ Processing failed: {result.get('error', 'Unknown error')}")
            if result.get('status_code'):
                st.caption(f"HTTP Status Code: {result['status_code']}")
            if result.get('debug_info'):
                with st.expander("🔍 Debug Information"):
                    st.text(result['debug_info'])


def render_results_tab():
    """Render the results tab with outputs"""
    if 'result' not in st.session_state:
        st.info("No results yet. Process a BRD to see outputs here.")
        return
    
    result = st.session_state['result']
    
    # Summary
    st.header("📊 Processing Summary")
    summary = utils.extract_project_summary(result)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        status = summary['status']
        status_icon = "✅" if status == "success" else "❌"
        st.metric("Status", f"{status_icon} {status.title()}")
    
    with col2:
        stages = len(summary.get('stages_completed', []))
        st.metric("Stages Completed", stages)
    
    with col3:
        if summary.get('timestamp'):
            st.metric("Completed At", summary['timestamp'][:19])
    
    # Stages completed
    if summary.get('stages_completed'):
        st.write("**Completed Stages:**")
        cols = st.columns(len(summary['stages_completed']))
        for idx, stage in enumerate(summary['stages_completed']):
            with cols[idx]:
                st.success(f"✓ {stage.replace('_', ' ').title()}")
    
    st.divider()
    
    # Show full response
    with st.expander("📄 View Full Response"):
        st.json(result)
    
    # Download button
    st.download_button(
        label="💾 Download Full Response",
        data=json.dumps(result, indent=2),
        file_name=f"brd_processing_result_{summary.get('timestamp', 'unknown')[:10]}.json",
        mime="application/json"
    )


def render_timeline_tab():
    """Render the timeline/Gantt chart tab"""
    if 'result' not in st.session_state:
        st.info("No timeline data yet. Process a BRD to see the project timeline here.")
        return
    
    st.header("📅 Project Timeline")
    
    result = st.session_state['result']
    
    # Note about where schedule data would be
    st.info("📌 **Note:** Timeline visualization requires project schedule data from the orchestrator response.")
    
    # Try to create Gantt chart from response
    # The actual schedule is saved to files, not returned in response
    # So we'll show a message about this
    
    with st.expander("ℹ️ About Timeline Data"):
        st.markdown("""
        The project schedule is generated and saved to:
        - `sample_inputs/outputs/project_schedules/`
        
        The timeline includes:
        - **Phases** - Major implementation phases
        - **Milestones** - Key deliverables and checkpoints
        - **Tasks** - Detailed task breakdown
        - **Resource Allocation** - Team assignments
        - **Critical Path** - Dependencies and blockers
        
        To view the full project schedule:
        1. Check the output directory for the generated JSON file
        2. The filename includes the project name and timestamp
        """)
    
    # Show message about accessing full schedule
    st.success("✅ Project schedule generated and saved to outputs directory")
    
    note_message = result.get("note", "")
    if note_message:
        st.caption(f"💡 {note_message}")


def clear_session():
    """Clear session state"""
    keys_to_clear = ['brd_data', 'brd_text', 'result', 'processing_complete']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()


def main():
    """Main application entry point"""
    # Initialize session state
    if 'processing_complete' not in st.session_state:
        st.session_state['processing_complete'] = False
    
    # Render header
    render_header()
    
    # Render sidebar and get config
    orchestrator_url = render_sidebar()
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["📝 Input & Process", "📊 Results", "📅 Timeline"])
    
    with tab1:
        brd_valid = render_input_tab()
        if brd_valid:
            st.divider()
            render_processing_section(orchestrator_url)
    
    with tab2:
        render_results_tab()
    
    with tab3:
        render_timeline_tab()
    
    # Footer
    st.divider()
    st.caption("🤖 BRD Agent v1.0 | Built with Streamlit, n8n & Anthropic Claude")


if __name__ == "__main__":
    main()

