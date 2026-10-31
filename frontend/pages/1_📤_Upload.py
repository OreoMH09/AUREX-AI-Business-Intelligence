"""
AUREX Upload Page
Document upload and ingestion interface
"""
import streamlit as st
from pathlib import Path
import sys
import httpx
import time

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.core import settings

st.set_page_config(
    page_title="Upload - AUREX",
    page_icon="📤",
    layout="wide"
)

st.title("📤 Document Upload")

st.markdown("""
Upload your business documents for analysis. Supported formats: PDF, Excel (.xlsx, .xls), CSV
""")

# Upload section
st.markdown("---")
st.markdown("### Upload Documents")

uploaded_files = st.file_uploader(
    "Choose files to upload",
    type=["pdf", "xlsx", "xls", "csv"],
    accept_multiple_files=True,
    help="Select one or more business documents"
)

if uploaded_files:
    st.info(f"📁 {len(uploaded_files)} file(s) selected")
    
    # Show selected files
    for file in uploaded_files:
        file_size_mb = len(file.getvalue()) / (1024 * 1024)
        st.text(f"• {file.name} ({file_size_mb:.2f} MB)")

if st.button("Upload and Process", disabled=not uploaded_files):
    if uploaded_files:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        uploaded_docs = []
        failed_docs = []
        
        for idx, file in enumerate(uploaded_files):
            try:
                status_text.text(f"Uploading {file.name}...")
                
                # Prepare file for upload
                files = {
                    "file": (file.name, file.getvalue(), file.type)
                }
                
                # Upload to API (increased timeout for large files)
                response = httpx.post(
                    f"http://{settings.api_host}:{settings.api_port}/api/upload",
                    files=files,
                    timeout=180.0  # 3 minutes - handles large CSV/Excel files
                )
                
                if response.status_code == 200:
                    data = response.json()
                    uploaded_docs.append(data)
                    status_text.text(f"✅ {file.name} uploaded successfully")
                else:
                    failed_docs.append(file.name)
                    status_text.text(f"❌ {file.name} failed to upload")
                
                # Update progress
                progress = (idx + 1) / len(uploaded_files)
                progress_bar.progress(progress)
                
                time.sleep(0.5)  # Brief pause for visual feedback
                
            except httpx.TimeoutException:
                failed_docs.append(file.name)
                st.error(f"⏱️ **Timeout uploading {file.name}**")
                st.info(f"""
                **This can happen with large files ({file.size / 1024 / 1024:.1f} MB).**
                
                **Tips:**
                - File is being processed in background, check back in 1-2 minutes
                - Try uploading one file at a time
                - For very large files, split into smaller chunks
                """)
            except Exception as e:
                failed_docs.append(file.name)
                st.error(f"Error uploading {file.name}: {str(e)}")
        
        progress_bar.empty()
        status_text.empty()
        
        # Show results
        if uploaded_docs:
            st.success(f"✅ Successfully uploaded {len(uploaded_docs)} document(s)")
            
            # Show document details
            for doc in uploaded_docs:
                with st.expander(f"📄 {doc['filename']}"):
                    st.write(f"**Document ID:** {doc['document_id']}")
                    st.write(f"**Type:** {doc['file_type']}")
                    st.write(f"**Size:** {doc['file_size_bytes'] / 1024:.2f} KB")
                    st.write(f"**Status:** {doc['status']}")
        
        if failed_docs:
            st.error(f"❌ Failed to upload {len(failed_docs)} document(s): {', '.join(failed_docs)}")

st.markdown("---")

# Document list section
st.markdown("### 📚 Uploaded Documents")

# Add refresh button and bulk actions
col_refresh, col_bulk, col_count = st.columns([1, 1, 3])
with col_refresh:
    if st.button("🔄 Refresh List"):
        st.rerun()

with col_bulk:
    if st.button("🗑️ Delete All", type="secondary"):
        if st.session_state.get('confirm_delete_all'):
            # Actually delete all
            try:
                with st.spinner("Deleting all documents..."):
                    response = httpx.get(
                        f"http://{settings.api_host}:{settings.api_port}/api/documents",
                        timeout=30.0
                    )
                    if response.status_code == 200:
                        documents = response.json()
                        deleted_count = 0
                        for doc in documents:
                            try:
                                del_response = httpx.delete(
                                    f"http://{settings.api_host}:{settings.api_port}/api/documents/{doc['document_id']}",
                                    timeout=10.0
                                )
                                if del_response.status_code == 200:
                                    deleted_count += 1
                            except:
                                pass
                        st.success(f"✅ Deleted {deleted_count} documents!")
                        st.session_state['confirm_delete_all'] = False
                        time.sleep(1)
                        st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
                st.session_state['confirm_delete_all'] = False
        else:
            st.session_state['confirm_delete_all'] = True
            st.warning("⚠️ Click again to confirm deleting ALL documents!")
            st.rerun()

try:
    with st.spinner("Loading documents..."):
        response = httpx.get(
            f"http://{settings.api_host}:{settings.api_port}/api/documents",
            timeout=30.0  # Increased timeout
        )
    
    if response.status_code == 200:
        documents = response.json()
        
        if documents:
            with col_count:
                st.info(f"📊 Total documents: **{len(documents)}** | Click 🗑️ to delete duplicates")
            
            # Add search/filter
            search_query = st.text_input("🔍 Search documents", placeholder="Type filename to search...")
            
            # Filter documents if search query provided
            if search_query:
                documents = [doc for doc in documents if search_query.lower() in doc['filename'].lower()]
                st.info(f"Showing {len(documents)} matching documents")
            
            # Group by filename to show duplicates
            filename_groups = {}
            for doc in documents:
                filename = doc['filename']
                if filename not in filename_groups:
                    filename_groups[filename] = []
                filename_groups[filename].append(doc)
            
            # Show documents grouped by filename
            for filename, docs in filename_groups.items():
                # Show duplicate warning if more than 1
                if len(docs) > 1:
                    st.warning(f"⚠️ **{filename}** - {len(docs)} copies found (DUPLICATE)")
                
                for idx, doc in enumerate(docs):
                    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
                    
                    with col1:
                        # Show if duplicate
                        duplicate_marker = f" (Copy {idx+1})" if len(docs) > 1 else ""
                        st.text(f"📄 {doc['filename']}{duplicate_marker}")
                        st.caption(f"ID: {doc['document_id'][:8]}...")
                    
                    with col2:
                        st.text(f"{doc['file_type'].upper()}")
                    
                    with col3:
                        size_kb = doc.get('file_size_bytes', 0) / 1024
                        st.text(f"{size_kb:.1f} KB")
                    
                    with col4:
                        status_icon = {
                            "pending": "⏳",
                            "processing": "🔄",
                            "completed": "✅",
                            "failed": "❌"
                        }.get(doc['status'], "❓")
                        st.text(f"{status_icon} {doc['status']}")
                    
                    with col5:
                        delete_label = "🗑️ Delete"
                        if st.button(delete_label, key=f"del_{doc['document_id']}", type="secondary"):
                            try:
                                with st.spinner(f"Deleting {doc['filename']}..."):
                                    del_response = httpx.delete(
                                        f"http://{settings.api_host}:{settings.api_port}/api/documents/{doc['document_id']}",
                                        timeout=10.0
                                    )
                                if del_response.status_code == 200:
                                    st.success(f"✅ Deleted {doc['filename']}!")
                                    time.sleep(0.5)
                                    st.rerun()
                                else:
                                    st.error(f"❌ Failed to delete: {del_response.text}")
                            except Exception as e:
                                st.error(f"❌ Error deleting: {str(e)}")
                    
                    st.divider()
                
        else:
            st.info("📭 No documents uploaded yet. Upload your first document above!")
    else:
        st.error(f"❌ API Error: {response.status_code}")
        st.code(response.text)
        
except httpx.TimeoutException:
    st.error("⏱️ **Timeout loading documents**")
    st.info("""
    **This can happen when you have many documents.**
    
    **What to do:**
    - Wait a moment and click "🔄 Refresh List"
    - Or restart AUREX: `RESTART_AUREX.bat`
    - Check if backend is running (Backend window should be open)
    """)
except Exception as e:
    st.warning(f"⚠️ Unable to connect to backend API")
    st.code(f"Error: {str(e)}")
    st.info("""
    **To start the backend server:**
    
    Run in terminal:
    ```bash
    START_AUREX.bat
    ```
    
    Or check if backend is already running:
    - Backend window should be open
    - Look for: "Started server process"
    """)

st.markdown("---")

# Information section
with st.expander("ℹ️ Upload Information"):
    st.markdown("""
    **Supported Formats:**
    - **PDF**: Business reports, financial statements, annual reports
    - **Excel (.xlsx, .xls)**: Sales data, financial data, product data
    - **CSV**: Structured datasets, transaction records
    
    **Processing Steps:**
    1. **Upload**: File is validated and saved
    2. **Ingestion**: Content is extracted and parsed
    3. **Indexing**: Data is embedded and stored (Coming in Stage 8)
    4. **Ready**: Document is ready for querying
    
    **File Limits:**
    - Maximum file size: 50 MB
    - Multiple files can be uploaded at once
    
    **Data Security:**
    - Files are stored securely in the upload directory
    - Only supported file types are accepted
    - Filenames are sanitized to prevent security issues
    """)

