"""
AUREX Reports Page
Business report generation and export
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
    page_title="Reports - AUREX",
    page_icon="📄",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .report-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .report-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .report-meta {
        color: #666;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("📄 Business Reports")
st.markdown("Generate professional business reports with automated insights")

# Sidebar configuration
with st.sidebar:
    st.markdown("### ⚙️ Report Configuration")
    
    report_type = st.selectbox(
        "Report Type",
        ["executive", "detailed", "summary"],
        format_func=lambda x: x.capitalize() + " Report"
    )
    
    document_filter = st.text_input(
        "Document ID (optional)",
        "",
        help="Leave empty to include all documents"
    )
    
    export_format = st.selectbox(
        "Export Format",
        ["html", "markdown", "json"],
        format_func=lambda x: x.upper()
    )
    
    st.markdown("---")
    st.markdown("### 📋 Report Sections")
    st.info("""
    **Executive Report:** Summary KPIs, insights, recommendations
    
    **Detailed Report:** Comprehensive analysis with all metrics
    
    **Summary Report:** Quick overview of key findings
    """)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Generate New Report")
    
    # Add demo mode toggle
    use_demo = st.checkbox(
        "⚡ Quick Demo Mode (Instant)",
        value=True,
        help="Generate report with sample data instantly. Uncheck to use real data (slower)."
    )
    
    report_title = st.text_input(
        "Report Title (optional)",
        placeholder="Leave empty for default title"
    )
    
    report_description = st.text_area(
        "Report Description (optional)",
        placeholder="Add any notes or context for this report"
    )
    
    generate_button = st.button(
        "🚀 Generate Report",
        type="primary",
        use_container_width=True
    )
    
    if generate_button:
        if use_demo:
            # INSTANT DEMO MODE - No backend call
            with st.spinner("Generating demo report..."):
                import time
                time.sleep(0.5)  # Simulate processing
                
                # Create demo report data
                from datetime import datetime
                report_data = {
                    "executive_summary": """
                    Business Performance Analysis for Q4 2024 demonstrates exceptional growth across all key metrics. 
                    Total revenue reached $2,847,650, representing a 12.5% increase year-over-year from $2,532,000 in 2023. 
                    Product A continues to lead the portfolio with $845,200 in sales (29.7% market share), while the North America 
                    region shows the strongest market presence at $1,245,000 (43.7% of total revenue). Profit margins improved 
                    significantly to 53.5% from 48.2% in 2023, indicating highly effective cost management and optimal pricing strategies. 
                    Q4 2024 marked the strongest quarterly performance of the year at $727,650, demonstrating positive momentum 
                    heading into 2025.
                    """,
                    "insights": [
                        "Revenue grew 12.5% compared to 2023 ($2,532,000 → $2,847,650), exceeding annual target by 8.2%",
                        "Product A dominates portfolio with 29.7% market share ($845,200), while Products C and D underperform at 15% and 12% respectively",
                        "North America region leads with 43.7% of total revenue ($1,245,000), followed by Europe at 28.3% ($806,000)",
                        "Profit margin improved from 48.2% to 53.5%, representing a 5.3 percentage point increase and industry-leading performance",
                        "Q4 2024 showed strongest quarterly performance ($727,650), indicating 18% quarter-over-quarter growth and positive market trends",
                        "Customer retention rate reached 87%, up from 82% in 2023, demonstrating strong product-market fit",
                        "Average order value increased 9.2% to $3,450, suggesting successful upselling and premium product adoption",
                        "Asia-Pacific region shows emerging growth potential with 22% YoY increase despite lower absolute revenue"
                    ],
                    "recommendations": [
                        "Expand Product A distribution channels and increase inventory allocation by 25% based on exceptional performance and market demand",
                        "Investigate root causes of underperformance in Products C and D - conduct customer feedback analysis and consider product refresh or discontinuation",
                        "Continue current cost optimization strategies to maintain industry-leading 53.5% profit margins while investing in growth initiatives",
                        "Increase marketing investment in Asia-Pacific region by 30% to capitalize on 22% growth momentum and establish market leadership early",
                        "Develop premium product line extensions leveraging Product A success to capture high-value customer segment and increase average order value",
                        "Implement targeted retention programs in Europe and South America where customer churn rates remain above company average",
                        "Launch pilot expansion program in top 3 underserved markets (Africa, South America, Middle East) with localized product offerings",
                        "Invest in sales team expansion in North America to maintain market leadership and prevent competitor encroachment"
                    ],
                    "kpis": {
                        "revenue": {"value": 2847650, "year": "2024"},
                        "profit": {"value": 1523400, "year": "2024"},
                        "margin": {"value": 53.5, "unit": "%"},
                        "growth": {"value": 12.5, "unit": "%"}
                    }
                }
                
                filename = f"demo_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                
                # Create HTML content for demo report
                html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Executive Business Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            color: #1f77b4;
            border-bottom: 3px solid #1f77b4;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #2c5282;
            margin-top: 30px;
        }}
        .meta {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 30px;
        }}
        .summary {{
            background: #f0f4f8;
            padding: 20px;
            border-left: 4px solid #1f77b4;
            margin: 20px 0;
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .kpi-card {{
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .kpi-value {{
            font-size: 2em;
            font-weight: bold;
            color: #1f77b4;
        }}
        .kpi-label {{
            color: #666;
            font-size: 0.9em;
        }}
        .insight {{
            background: #fff3cd;
            padding: 10px 15px;
            margin: 10px 0;
            border-left: 3px solid #ffc107;
        }}
        .recommendation {{
            background: #d4edda;
            padding: 10px 15px;
            margin: 10px 0;
            border-left: 3px solid #28a745;
        }}
    </style>
</head>
<body>
    <h1>Executive Business Report</h1>
    <div class="meta">
        Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
    </div>
    
    <h2>Executive Summary</h2>
    <div class="summary">
        {report_data['executive_summary'].strip()}
    </div>
    
    <h2>Key Performance Indicators</h2>
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Revenue</div>
            <div class="kpi-value">${report_data['kpis']['revenue']['value']:,.0f}</div>
            <div class="kpi-label">Year: {report_data['kpis']['revenue']['year']}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Profit</div>
            <div class="kpi-value">${report_data['kpis']['profit']['value']:,.0f}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Profit Margin</div>
            <div class="kpi-value">{report_data['kpis']['margin']['value']}%</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Growth Rate</div>
            <div class="kpi-value">{report_data['kpis']['growth']['value']}%</div>
        </div>
    </div>
    
    <h2>Key Insights</h2>
"""
                for insight in report_data['insights']:
                    html_content += f'    <div class="insight">💡 {insight}</div>\n'
                
                html_content += """
    <h2>Recommendations</h2>
"""
                for rec in report_data['recommendations']:
                    html_content += f'    <div class="recommendation">✅ {rec}</div>\n'
                
                html_content += """
</body>
</html>
"""
                
                # Save demo HTML file
                from pathlib import Path
                reports_dir = Path("data/reports")
                reports_dir.mkdir(parents=True, exist_ok=True)
                report_path = reports_dir / filename
                with open(report_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                result = {
                    "success": True,
                    "filename": filename,
                    "report_data": report_data,
                    "demo_mode": True
                }
        else:
            # REAL DATA MODE - Backend call with optimized timeout
            spinner_msg = "Generating report... This may take 3-5 minutes for real data" if not use_demo else "Generating report..."
            with st.spinner(spinner_msg):
                try:
                    # Prepare request
                    request_data = {
                        "report_type": report_type,
                        "format": export_format
                    }
                    
                    if document_filter:
                        request_data["document_id"] = document_filter
                    
                    # Generate report with extended timeout - 5 MINUTES for complete processing
                    response = httpx.post(
                        f"http://{settings.api_host}:{settings.api_port}/api/reports/generate",
                        json=request_data,
                        timeout=300.0  # 5 minutes - allows multiple LLM calls
                    )
                
                    if response.status_code == 200:
                        result = response.json()
                    else:
                        st.error(f"❌ Error: {response.status_code} - {response.text}")
                        result = None
                        
                except httpx.TimeoutException:
                    st.error("⏱️ Request timed out. Report generation took more than 5 minutes.")
                    st.info("""
                    **Tip:** Enable "⚡ Quick Demo Mode" for instant reports with sample data.
                    Real data processing can take 3-5 minutes for large datasets with multiple LLM calls.
                    """)
                    result = None
                except httpx.ConnectError:
                    st.error("🔌 Cannot connect to backend API. Please ensure the server is running.")
                    result = None
                except Exception as e:
                    st.error(f"❌ Error generating report: {str(e)}")
                    result = None
        
        # Display results (common for both demo and real)
        if result and result.get('success'):
            # Show success message
            demo_badge = " (Demo Mode)" if result.get('demo_mode') else ""
            st.success(f"✅ Report generated successfully{demo_badge}: {result['filename']}")
            
            # Display report data
            with st.expander("📊 Report Preview", expanded=True):
                report_data = result.get('report_data', {})
                
                # Show KPIs if available
                if 'kpis' in report_data:
                    st.markdown("#### Key Performance Indicators")
                    kpis = report_data['kpis']
                    col_a, col_b, col_c, col_d = st.columns(4)
                    
                    with col_a:
                        if 'revenue' in kpis:
                            rev_val = kpis['revenue'].get('value', kpis['revenue']) if isinstance(kpis['revenue'], dict) else kpis['revenue']
                            rev_year = kpis['revenue'].get('year', 'N/A') if isinstance(kpis['revenue'], dict) else 'N/A'
                            st.metric("Total Revenue", f"${float(rev_val):,.0f}", 
                                     f"Year: {rev_year}")
                    
                    with col_b:
                        if 'profit' in kpis:
                            profit_val = kpis['profit'].get('value', kpis['profit']) if isinstance(kpis['profit'], dict) else kpis['profit']
                            st.metric("Profit", f"${float(profit_val):,.0f}")
                    
                    with col_c:
                        if 'margin' in kpis:
                            margin_val = kpis['margin'].get('value', kpis['margin']) if isinstance(kpis['margin'], dict) else kpis['margin']
                            st.metric("Profit Margin", f"{float(margin_val):.1f}%")
                    
                    with col_d:
                        if 'growth' in kpis:
                            growth_val = kpis['growth'].get('value', kpis['growth']) if isinstance(kpis['growth'], dict) else kpis['growth']
                            # Handle nested dict or direct value
                            if isinstance(growth_val, dict):
                                growth_val = growth_val.get('growth_rate', growth_val.get('growth', growth_val.get('value', 0)))
                            try:
                                growth_val = float(growth_val or 0)
                            except (TypeError, ValueError):
                                growth_val = 0.0
                            st.metric("Growth Rate", f"{growth_val:.1f}%")
                    
                    st.markdown("---")
                
                if 'executive_summary' in report_data:
                    st.markdown("#### Executive Summary")
                    st.write(report_data['executive_summary'])
                
                if 'insights' in report_data:
                    st.markdown("#### Key Insights")
                    for insight in report_data['insights']:
                        st.info(f"💡 {insight}")
                
                if 'recommendations' in report_data:
                    st.markdown("#### Recommendations")
                    for rec in report_data['recommendations']:
                        st.success(f"✅ {rec}")
            
            # Download buttons
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if result.get('demo_mode'):
                    st.info("📥 Download available in real data mode")
                else:
                    download_url = f"http://{settings.api_host}:{settings.api_port}/api/reports/download/{result['filename']}"
                    st.markdown(f"[⬇️ Download Report]({download_url})")
            
            with col_b:
                if export_format == 'html' and not result.get('demo_mode'):
                    preview_url = f"http://{settings.api_host}:{settings.api_port}/api/reports/preview/{result['filename']}"
                    st.markdown(f"[👁️ Preview in Browser]({preview_url})")
            
            with col_c:
                if result.get('demo_mode'):
                    st.info("💡 Uncheck Demo Mode for real data")
        elif result:
            st.error(f"❌ Report generation failed: {result.get('error', 'Unknown error')}")

with col2:
    st.markdown("### 💡 Tips")
    st.info("""
    **For best results:**
    - Ensure documents are uploaded and processed
    - Executive reports are quick to generate
    - Detailed reports include more analysis
    - HTML reports have better formatting
    """)
    
    st.markdown("### 📊 Report Contents")
    
    if report_type == 'executive':
        st.markdown("""
        - Executive Summary
        - Key KPIs
        - Top Insights
        - Recommendations
        """)
    elif report_type == 'detailed':
        st.markdown("""
        - Comprehensive Summary
        - All KPIs
        - Product Analysis
        - Regional Analysis
        - Trend Analysis
        - Detailed Insights
        - Full Recommendations
        """)
    else:
        st.markdown("""
        - Quick Summary
        - Essential KPIs
        - Key Takeaways
        """)

st.markdown("---")

# Recent reports section
st.markdown("### 📋 Recent Reports")

reports_dir = Path("data/reports")
if reports_dir.exists():
    report_files = sorted(
        reports_dir.glob("*"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )[:10]  # Show last 10 reports
    
    if report_files:
        for report_file in report_files:
            col_a, col_b, col_c, col_d = st.columns([3, 1, 1, 1])
            
            with col_a:
                st.markdown(f"**{report_file.name}**")
                modified_time = datetime.fromtimestamp(report_file.stat().st_mtime)
                st.caption(f"Created: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            with col_b:
                download_url = f"http://{settings.api_host}:{settings.api_port}/api/reports/download/{report_file.name}"
                st.markdown(f"[⬇️ Download]({download_url})")
            
            with col_c:
                if report_file.suffix == '.html':
                    preview_url = f"http://{settings.api_host}:{settings.api_port}/api/reports/preview/{report_file.name}"
                    st.markdown(f"[👁️ Preview]({preview_url})")
            
            with col_d:
                if st.button("🗑️ Delete", key=f"delete_{report_file.name}"):
                    try:
                        delete_response = httpx.delete(
                            f"http://{settings.api_host}:{settings.api_port}/api/reports/{report_file.name}",
                            timeout=10.0
                        )
                        if delete_response.status_code == 200:
                            st.success(f"✅ Deleted {report_file.name}")
                            st.rerun()
                        else:
                            st.error(f"❌ Failed to delete: {delete_response.text}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            
            st.markdown("---")
    else:
        st.info("No reports generated yet. Create your first report above!")
else:
    st.info("No reports directory found. Reports will be saved to data/reports/")

# Footer
st.markdown("---")
st.caption("💡 Reports are saved locally and can be accessed anytime from the Recent Reports section.")
