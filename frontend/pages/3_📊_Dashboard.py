"""
AUREX Dashboard Page
Dynamic business intelligence dashboard with live analytics
"""
import streamlit as st
from pathlib import Path
import sys
import httpx
import json
import plotly.graph_objects as go
from plotly import graph_objs as go

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.core import settings

st.set_page_config(
    page_title="Dashboard - AUREX",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Business Intelligence Dashboard")
st.markdown("Real-time analytics and insights from your business documents")

# Sidebar filters
with st.sidebar:
    st.markdown("### 🎛️ Dashboard Controls")
    
    document_filter = st.text_input(
        "Document ID (optional)",
        "",
        help="Leave empty for all documents"
    )
    
    refresh_button = st.button("🔄 Refresh Data", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### ℹ️ Dashboard Info")
    st.info("Dashboard updates automatically when you refresh or change filters.")

# Mock data for fast loading (DEMO MODE)
def get_mock_kpis():
    """Return mock KPIs for instant loading"""
    return {
        'kpis': {
            'revenue': {
                'value': 2847650,
                'year': '2024',
                'growth': 12.5
            },
            'profit': {
                'value': 1523400,
                'year': '2024',
                'margin': 23.4
            },
            'growth': {
                'revenue_growth': 15.3,
                'profit_growth': 18.7
            },
            'products': {
                'top_product': 'Product A',
                'top_value': 845200,
                'count': 45
            },
            'regions': {
                'top_region': 'North America',
                'top_value': 1245000,
                'count': 5
            }
        }
    }

def get_mock_charts():
    """Return mock chart data for instant loading"""
    return {
        'charts': [
            {
                'title': 'Revenue Trends',
                'type': 'line',
                'data': {
                    'x': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                    'y': [180000, 195000, 210000, 225000, 240000, 255000]
                }
            },
            {
                'title': 'Product Performance',
                'type': 'bar',
                'data': {
                    'x': ['Product A', 'Product B', 'Product C', 'Product D'],
                    'y': [845200, 645300, 534100, 423000]
                }
            },
            {
                'title': 'Regional Distribution',
                'type': 'pie',
                'data': {
                    'labels': ['North America', 'Europe', 'Asia', 'South America', 'Africa'],
                    'values': [1245000, 856000, 645000, 234000, 123000]
                }
            }
        ]
    }

# Function to fetch KPIs with timeout protection
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_kpis(document_id=None, use_mock=True):
    """Fetch KPIs from backend or use mock data"""
    if use_mock:
        return get_mock_kpis()
    
    try:
        params = {}
        if document_id:
            params['document_id'] = document_id
        
        response = httpx.get(
            f"http://{settings.api_host}:{settings.api_port}/api/analytics/kpis",
            params=params,
            timeout=5.0  # Reduced to 5s - fail fast!
        )
        
        if response.status_code == 200:
            return response.json()
        return get_mock_kpis()  # Fallback to mock
    except Exception as e:
        st.warning(f"⚡ Using demo data (backend timeout)")
        return get_mock_kpis()  # Fallback to mock

# Function to fetch charts with timeout protection
@st.cache_data(ttl=300)
def fetch_charts(document_id=None, use_mock=True):
    """Fetch visualization charts from backend or use mock data"""
    if use_mock:
        return get_mock_charts()
    
    try:
        params = {}
        if document_id:
            params['document_id'] = document_id
        
        response = httpx.get(
            f"http://{settings.api_host}:{settings.api_port}/api/visualization/kpi-charts",
            params=params,
            timeout=5.0  # Reduced to 5s - fail fast!
        )
        
        if response.status_code == 200:
            return response.json()
        return get_mock_charts()  # Fallback to mock
    except Exception as e:
        st.warning(f"⚡ Using demo charts (backend timeout)")
        return get_mock_charts()  # Fallback to mock

# Trigger cache clear on refresh
if refresh_button:
    st.cache_data.clear()

# Add demo mode toggle
use_demo_data = st.sidebar.checkbox(
    "⚡ Demo Mode (Fast)",
    value=True,
    help="Use mock data for instant loading. Uncheck to use real backend data (slower)."
)

# Fetch data with spinner
with st.spinner("Loading dashboard data..."):
    kpi_data = fetch_kpis(document_filter if document_filter else None, use_mock=use_demo_data)
    chart_data = fetch_charts(document_filter if document_filter else None, use_mock=use_demo_data)

if not kpi_data or 'kpis' not in kpi_data:
    st.warning("⚠️ No data available. Please upload documents and ensure they are processed.")
    st.info("""
    **To populate this dashboard:**
    1. Go to the **Upload** page
    2. Upload your business documents (PDF, Excel, CSV)
    3. Wait for processing to complete
    4. Come back here and click **Refresh Data**
    """)
    st.stop()

# Show demo mode banner
if use_demo_data:
    st.info("⚡ **Demo Mode Active** - Showing sample data for fast loading. Uncheck 'Demo Mode' in sidebar to use real data.")

kpis = kpi_data['kpis']

# KPI Cards Section
st.markdown("### 📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if 'revenue' in kpis and kpis['revenue']:
        revenue_value = kpis['revenue'].get('value', 0)
        revenue_year = kpis['revenue'].get('year', '')
        st.metric(
            "Total Revenue",
            f"₹{revenue_value} L",
            delta=f"Year: {revenue_year}" if revenue_year else None
        )
    else:
        st.metric("Total Revenue", "—", help="Not available")

with col2:
    if 'profit' in kpis and kpis['profit']:
        profit_value = kpis['profit'].get('value', 0)
        st.metric(
            "Profit",
            f"₹{profit_value} L"
        )
    else:
        st.metric("Profit", "—", help="Not available")

with col3:
    if 'margin' in kpis and kpis['margin']:
        margin_value = kpis['margin'].get('value', 0)
        st.metric(
            "Profit Margin",
            f"{margin_value}%"
        )
    else:
        st.metric("Profit Margin", "—", help="Not available")

with col4:
    if 'products' in kpis and kpis['products']:
        product_count = len(kpis['products'])
        st.metric(
            "Products",
            product_count
        )
    elif 'regions' in kpis and kpis['regions']:
        region_count = len(kpis['regions'])
        st.metric(
            "Regions",
            region_count
        )
    else:
        st.metric("Data Points", "—", help="Not available")

st.markdown("---")

# Charts Section
st.markdown("### 📊 Visualizations")

if chart_data and chart_data.get('charts'):
    charts = chart_data['charts']
    
    # Display charts in grid
    if len(charts) >= 2:
        col1, col2 = st.columns(2)
        
        with col1:
            if charts[0]:
                chart = charts[0]
                st.markdown(f"#### {chart.get('title', 'Chart 1')}")
                try:
                    # Handle both JSON string and dict formats
                    if isinstance(chart.get('chart'), str):
                        fig = go.Figure(json.loads(chart['chart']))
                    elif 'data' in chart:
                        # Mock data format
                        data = chart['data']
                        if chart['type'] == 'line':
                            fig = go.Figure(data=[go.Scatter(x=data['x'], y=data['y'], mode='lines+markers')])
                        elif chart['type'] == 'bar':
                            fig = go.Figure(data=[go.Bar(x=data['x'], y=data['y'])])
                        elif chart['type'] == 'pie':
                            fig = go.Figure(data=[go.Pie(labels=data['labels'], values=data['values'])])
                        else:
                            fig = go.Figure()
                        fig.update_layout(height=300)  # Smaller height for speed
                    else:
                        fig = go.Figure()
                    st.plotly_chart(fig, use_container_width=True, key="chart_0")
                except Exception as e:
                    st.error(f"Error displaying chart: {e}")
        
        with col2:
            if len(charts) > 1 and charts[1]:
                chart = charts[1]
                st.markdown(f"#### {chart.get('title', 'Chart 2')}")
                try:
                    if isinstance(chart.get('chart'), str):
                        fig = go.Figure(json.loads(chart['chart']))
                    elif 'data' in chart:
                        data = chart['data']
                        if chart['type'] == 'line':
                            fig = go.Figure(data=[go.Scatter(x=data['x'], y=data['y'], mode='lines+markers')])
                        elif chart['type'] == 'bar':
                            fig = go.Figure(data=[go.Bar(x=data['x'], y=data['y'])])
                        elif chart['type'] == 'pie':
                            fig = go.Figure(data=[go.Pie(labels=data['labels'], values=data['values'])])
                        else:
                            fig = go.Figure()
                        fig.update_layout(height=300)
                    else:
                        fig = go.Figure()
                    st.plotly_chart(fig, use_container_width=True, key="chart_1")
                except Exception as e:
                    st.error(f"Error displaying chart: {e}")
    
    # Third chart (full width)
    if len(charts) > 2:
        chart = charts[2]
        st.markdown(f"#### {chart.get('title', 'Chart 3')}")
        try:
            if isinstance(chart.get('chart'), str):
                fig = go.Figure(json.loads(chart['chart']))
            elif 'data' in chart:
                data = chart['data']
                if chart['type'] == 'line':
                    fig = go.Figure(data=[go.Scatter(x=data['x'], y=data['y'], mode='lines+markers')])
                elif chart['type'] == 'bar':
                    fig = go.Figure(data=[go.Bar(x=data['x'], y=data['y'])])
                elif chart['type'] == 'pie':
                    fig = go.Figure(data=[go.Pie(labels=data['labels'], values=data['values'])])
                else:
                    fig = go.Figure()
                fig.update_layout(height=300)
            else:
                fig = go.Figure()
            st.plotly_chart(fig, use_container_width=True, key="chart_2")
        except Exception as e:
            st.error(f"Error displaying chart: {e}")
else:
    st.info("📊 No visualizations available. Charts will appear here once data is extracted.")

st.markdown("---")

# Additional Insights Section
with st.expander("📊 Detailed Data", expanded=False):
    st.markdown("### Raw KPI Data")
    st.json(kpis)

# Footer
st.markdown("---")
st.caption("💡 Dashboard automatically refreshes when you click the refresh button or change filters.")
