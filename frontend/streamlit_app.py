"""
AUREX Streamlit Frontend
Main application entry point
"""
import streamlit as st
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core import settings

# Page configuration
st.set_page_config(
    page_title="AUREX - AI Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-box {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.875rem;
        font-weight: 600;
    }
    .status-healthy {
        background-color: #d4edda;
        color: #155724;
    }
    .status-warning {
        background-color: #fff3cd;
        color: #856404;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/1f77b4/ffffff?text=AUREX", width=200)
    st.markdown("---")
    
    st.markdown("### 🎯 Navigation")
    st.info("Use the pages menu above to navigate through different sections of AUREX")
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown(f"""
    **Version:** {settings.app_version}  
    **Environment:** {settings.environment}  
    **LLM Provider:** {settings.llm_provider}  
    **Vector DB:** {settings.vector_db}
    """)

# Main content
st.markdown('<div class="main-header">📊 AUREX</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Multimodal RAG-Based Business Intelligence and Decision Support System</div>',
    unsafe_allow_html=True
)

# Introduction
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="feature-box">', unsafe_allow_html=True)
    st.markdown("### 📄 Multi-Format Support")
    st.markdown("""
    Upload and analyze business data from:
    - PDF Documents
    - Excel Spreadsheets
    - CSV Files
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="feature-box">', unsafe_allow_html=True)
    st.markdown("### 🤖 AI-Powered Analysis")
    st.markdown("""
    Natural language business questions with:
    - RAG-based retrieval
    - Automated analytics
    - Evidence-grounded insights
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="feature-box">', unsafe_allow_html=True)
    st.markdown("### 📈 Visual Intelligence")
    st.markdown("""
    On-demand visualizations:
    - Interactive charts
    - Dynamic dashboards
    - Professional reports
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# System Status
st.markdown("### 🔧 System Status")

try:
    import httpx
    response = httpx.get(f"http://{settings.api_host}:{settings.api_port}/api/health", timeout=5.0)
    if response.status_code == 200:
        health_data = response.json()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("API Status", health_data.get("status", "unknown").upper())
        
        with col2:
            st.metric("Version", health_data.get("version", "N/A"))
        
        with col3:
            st.metric("Environment", health_data.get("environment", "N/A"))
        
        with col4:
            services = health_data.get("services", {})
            healthy_services = sum(1 for v in services.values() if v in ["healthy", "operational"])
            st.metric("Services", f"{healthy_services}/{len(services)}")
        
        # Services details
        if services:
            st.markdown("#### Services Status")
            service_cols = st.columns(len(services))
            for idx, (service, status) in enumerate(services.items()):
                with service_cols[idx]:
                    status_class = "status-healthy" if status in ["healthy", "operational"] else "status-warning"
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <strong>{service.replace('_', ' ').title()}</strong><br>
                        <span class="status-badge {status_class}">{status}</span>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.error("⚠️ API is not responding correctly")
        
except Exception as e:
    st.warning(f"⚠️ Unable to connect to backend API. Please ensure the FastAPI server is running on port {settings.api_port}")
    st.code(f"Error: {str(e)}")
    st.info("""
    **To start the backend server:**
    ```bash
    python app/main.py
    ```
    """)

st.markdown("---")

# Quick Start Guide
st.markdown("### 🚀 Quick Start Guide")

st.markdown("""
1. **Upload Documents**: Go to the Upload page and add your business documents (PDF, Excel, CSV)
2. **Ask Questions**: Navigate to AI Business Analyst and ask natural language questions
3. **View Dashboards**: Check the Dashboard page for visual analytics
4. **Generate Reports**: Create comprehensive business reports with evidence and insights

**Example Questions:**
- "What was the total revenue in 2025?"
- "Compare this year's sales with last year"
- "Show me monthly revenue trends"
- "Which product had the highest sales?"
- "What happens if expenses increase by 10%?"
""")

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <strong>AUREX</strong> - AI Business Intelligence System<br>
    Built with RAG, LangChain, FastAPI & Streamlit<br>
    <em>Evidence-grounded insights for data-driven decisions</em>
</div>
""", unsafe_allow_html=True)
