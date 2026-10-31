"""
AUREX AI Business Analyst Page
Natural language query interface with RAG
"""
import streamlit as st
from pathlib import Path
import sys
import httpx
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.core import settings

st.set_page_config(
    page_title="AI Business Analyst - AUREX",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .source-box {
        padding: 1rem;
        border-left: 3px solid #1f77b4;
        background-color: #f8f9fa;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .metric-card {
        padding: 1rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
    }
    .example-question {
        padding: 0.5rem 1rem;
        background-color: #e7f3ff;
        border-left: 3px solid #2196F3;
        margin: 0.5rem 0;
        border-radius: 5px;
        cursor: pointer;
    }
    .example-question:hover {
        background-color: #d0e8ff;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI Business Analyst")
st.markdown("Ask natural language questions about your business documents")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_healthy" not in st.session_state:
    st.session_state.rag_healthy = None

# Check RAG health
def check_rag_health():
    """Check if RAG system is ready"""
    try:
        response = httpx.get(
            f"http://{settings.api_host}:{settings.api_port}/api/rag-health",
            timeout=5.0
        )
        if response.status_code == 200:
            health_data = response.json()
            return health_data
        return None
    except Exception as e:
        return None

# System status at the top
with st.expander("🔧 System Status", expanded=False):
    health = check_rag_health()
    
    if health:
        st.session_state.rag_healthy = health.get("overall") == "healthy"
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status = health.get("vector_store", "unknown")
            emoji = "✅" if status == "healthy" else "⚠️"
            st.markdown(f"**Vector Store:** {emoji} {status}")
            chunks = health.get("vector_store_chunks", 0)
            st.caption(f"{chunks} chunks stored")
        
        with col2:
            status = health.get("llm", "unknown")
            emoji = "✅" if status == "healthy" else "⚠️"
            st.markdown(f"**LLM (Ollama):** {emoji} {status}")
            st.caption(f"Model: {settings.ollama_model}")
        
        with col3:
            overall = health.get("overall", "unknown")
            emoji = "✅" if overall == "healthy" else "⚠️"
            st.markdown(f"**Overall:** {emoji} {overall}")
    else:
        st.session_state.rag_healthy = False
        st.error("⚠️ RAG system is not ready. Please ensure backend is running and Ollama is installed.")
        st.markdown("""
        **Requirements:**
        1. Backend API must be running
        2. Ollama must be installed and running
        3. Documents must be uploaded
        
        **To start Ollama:**
        ```bash
        ollama serve
        ollama pull llama3.1:8b
        ```
        """)

st.markdown("---")

# Main layout
chat_col, sidebar_col = st.columns([2, 1])

with sidebar_col:
    st.markdown("### 💡 Example Questions")
    
    example_questions = [
        "Create the graph of this year and last year profit",
        "Show me revenue trend over time",
        "Create a bar chart comparing products",
        "What was the total revenue in 2025?",
        "How much did profit margins improve?",
        "Which product had the highest sales?",
        "Which region showed the fastest growth?",
        "Generate a visualization of regional performance",
    ]
    
    st.markdown("Click on a question to ask:")
    for i, question in enumerate(example_questions):
        if st.button(question, key=f"example_{i}", use_container_width=True):
            st.session_state.selected_question = question
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Query Settings")
    top_k = st.slider("Documents to retrieve", 1, 10, 5, help="Number of relevant chunks to retrieve")
    
    st.markdown("---")
    
    st.markdown("### 📚 Document Filter")
    st.info("Filter by specific document (optional)")
    document_filter = st.text_input("Document ID", "", help="Leave empty to search all documents")

with chat_col:
    # Display chat history
    st.markdown("### 💬 Conversation")
    
    chat_container = st.container(height=400)
    
    with chat_container:
        if not st.session_state.messages:
            st.chat_message("assistant").write(
                "👋 Hello! I'm AUREX, your AI Business Analyst. "
                "I can help you analyze your business documents and answer questions based on the data. "
                "Upload some documents first, then ask me anything!"
            )
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Display chart if available
                if message["role"] == "assistant" and "chart" in message and message["chart"]:
                    chart_data = message["chart"]
                    st.markdown(f"### 📊 {chart_data.get('title', 'Generated Chart')}")
                    
                    try:
                        import json
                        chart_json = json.loads(chart_data['chart'])
                        st.plotly_chart(chart_json, use_container_width=True)
                    except Exception as chart_err:
                        st.error(f"Error displaying chart: {chart_err}")
                
                # Display sources if available
                if message["role"] == "assistant" and "sources" in message:
                    with st.expander("📎 Sources", expanded=False):
                        for source in message["sources"]:
                            st.markdown(f"""
                            <div class="source-box">
                                <strong>Source {source['source_id']}</strong> 
                                (Score: {source['score']}, Document: {source['document_id']})
                                <br><small>{source['content_preview']}</small>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Display metadata if available
                if message["role"] == "assistant" and "metadata" in message:
                    meta = message["metadata"]
                    st.caption(
                        f"Retrieved {meta.get('retrieved_chunks', 0)} chunks • "
                        f"Processed in {meta.get('processing_time_ms', 0)}ms" +
                        (" • 📊 Chart generated" if "chart" in message and message["chart"] else "")
                    )

# Query input - ALWAYS enabled now
query_input = st.chat_input(
    "Ask a business question...",
    disabled=False  # Always allow input
)

# Handle selected example question
if "selected_question" in st.session_state:
    query_input = st.session_state.selected_question
    del st.session_state.selected_question

# Process query
if query_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": query_input})
    
    # Display user message
    with chat_container:
        st.chat_message("user").write(query_input)
    
    # Query the RAG system
    with st.spinner("🤔 Thinking..."):
        try:
            # Prepare request
            request_data = {
                "question": query_input,
                "top_k": top_k
            }
            
            if document_filter:
                request_data["document_filter"] = document_filter
            
            # Send query to backend - WAIT UP TO 120 SECONDS for complete answer
            response = httpx.post(
                f"http://{settings.api_host}:{settings.api_port}/api/query",
                json=request_data,
                timeout=120.0  # 2 minutes - let LLM complete the answer
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Add assistant message
                assistant_message = {
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result.get("sources", []),
                    "metadata": {
                        "retrieved_chunks": result.get("retrieved_chunks", 0),
                        "processing_time_ms": result.get("processing_time_ms", 0)
                    }
                }
                
                # Add chart if generated
                if result.get("chart"):
                    assistant_message["chart"] = result["chart"]
                
                st.session_state.messages.append(assistant_message)
                
                # Rerun to display the new message
                st.rerun()
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
                
        except httpx.TimeoutException:
            st.error("⏱️ Request timed out. The query is taking too long. Please try a simpler question.")
        except httpx.ConnectError:
            st.error("🔌 Cannot connect to backend API. Please ensure the server is running.")
        except Exception as e:
            st.error(f"❌ Error processing query: {str(e)}")

# Clear chat button
if st.session_state.messages:
    if st.button("🗑️ Clear Conversation", type="secondary"):
        st.session_state.messages = []
        st.rerun()

st.markdown("---")

# Footer info
st.info("""
**💡 Tips for better results:**
- Upload documents first before asking questions
- Ask specific questions about data in your documents
- Use exact terms from your documents when possible
- Check the sources to verify the AI's answers
""")
