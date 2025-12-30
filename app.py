"""
RevStaff Full Funnel Metrics Dashboard
Streamlit app for viewing interactive SQL funnel charts
"""

import streamlit as st
from pathlib import Path

# Page config
st.set_page_config(
    page_title="RevStaff Metrics",
    page_icon="📊",
    layout="wide"
)

# Chart definitions
CHARTS = {
    "View 1: Volume Overview": {
        "1.3 SQL Volume by Source by Month": "chart-1-sqls-by-source.html"
    },
    "View 2: Rep Performance": {
        "2.0 Total SQLs per Rep per Month": "chart-3-total-sqls-per-rep.html",
        "2.1 Prospecting + Conference Distribution": "chart-2-overall-distribution.html",
        "2.2 Per-Rep Distribution Comparison": "chart-4-by-rep-distribution.html",
        "Rep-Level Boxplots": "chart-view2-by-rep-boxplots.html"
    },
    "View 2.3-2.4: Account Tier": {
        "2.3 Tier 1 Prospecting": "chart-5-t1-prospecting.html",
        "2.4 Non-Tier 1 Prospecting": "chart-6-non-t1-prospecting.html",
        "Tier 1 vs Non-Tier 1 by Month": "chart-t1-by-month.html",
        "Tier 1 vs Non-Tier 1 per Rep": "chart-t1-per-rep.html"
    },
    "View 2.5-2.8: By Source": {
        "2.5 Conference Distribution": "chart-7-conference-distribution.html",
        "2.7 Demo Request (Inbound)": "chart-9-demo-request.html",
        "2.8 Referrals": "chart-10-referrals.html"
    }
}

# Get charts directory (relative to app.py)
CHARTS_DIR = Path(__file__).parent / "charts"

def load_chart_html(filename):
    """Load HTML content from chart file"""
    filepath = CHARTS_DIR / filename
    if filepath.exists():
        return filepath.read_text()
    return f"<p>Chart not found: {filename}</p>"

# Sidebar
st.sidebar.title("📊 RevStaff Metrics")
st.sidebar.markdown("**2025 Performance Analysis**")
st.sidebar.markdown("Data through Dec 29 | n=416 SQLs")
st.sidebar.divider()

# Build flat list for selection
all_charts = []
for section, charts in CHARTS.items():
    for chart_name, filename in charts.items():
        all_charts.append((section, chart_name, filename))

# Section filter
sections = list(CHARTS.keys())
selected_section = st.sidebar.selectbox("Section", ["All"] + sections)

# Filter charts by section
if selected_section == "All":
    filtered_charts = all_charts
else:
    filtered_charts = [(s, n, f) for s, n, f in all_charts if s == selected_section]

# Chart selector
chart_names = [name for _, name, _ in filtered_charts]
selected_chart_name = st.sidebar.selectbox("Chart", chart_names)

# Find the selected chart
selected_chart = next((c for c in filtered_charts if c[1] == selected_chart_name), None)

st.sidebar.divider()
st.sidebar.markdown("*Cohort Month methodology*")
st.sidebar.markdown("[View source data →](https://github.com/baoyama/medscout-gtm)")

# Main content
if selected_chart:
    section, chart_name, filename = selected_chart

    # Header
    st.markdown(f"### {chart_name}")
    st.caption(f"{section}")

    # Load and display chart
    html_content = load_chart_html(filename)

    # Remove the navigation header we added (since Streamlit has its own nav)
    # Find and remove the div with "Back to Dashboard"
    if 'Back to Dashboard' in html_content:
        # Simple removal of the nav div
        start = html_content.find('<div style="font-family: Inter')
        if start != -1:
            end = html_content.find('</div>', start) + 6
            html_content = html_content[:start] + html_content[end:]

    # Display with appropriate height
    st.components.v1.html(html_content, height=600, scrolling=True)

else:
    st.info("Select a chart from the sidebar")
