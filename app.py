"""
RevStaff Full Funnel Metrics Dashboard
Streamlit app with card-based navigation
"""

import streamlit as st
from pathlib import Path

# Page config
st.set_page_config(
    page_title="RevStaff Metrics",
    page_icon="📊",
    layout="wide"
)

# Chart definitions organized by section
SECTIONS = {
    "View 1: Volume Overview": [
        {
            "id": "1.3",
            "title": "SQL Volume by Source by Month",
            "desc": "Stacked bar chart showing monthly SQL breakdown by source: Prospecting, Demo Request, Conference, Referral, Other",
            "tag": "Stacked Bar",
            "file": "chart-1-sqls-by-source.html"
        }
    ],
    "View 2: Rep Performance Distributions": [
        {
            "id": "2.0",
            "title": "Total SQLs per Rep per Month",
            "desc": "Box plot showing distribution of all SQLs per ramped rep per month with TARGET: 15 reference line",
            "tag": "Box + Strip Plot",
            "file": "chart-3-total-sqls-per-rep.html"
        },
        {
            "id": "2.1",
            "title": "Prospecting + Conference Distribution",
            "desc": "Box plot showing distribution of rep-driven SQLs (Prospecting + Conference) per ramped rep per month",
            "tag": "Box + Strip Plot",
            "file": "chart-2-overall-distribution.html"
        },
        {
            "id": "2.2",
            "title": "Per-Rep Distribution Comparison",
            "desc": "Side-by-side box plots showing SQL distribution by individual rep for consistency analysis",
            "tag": "Multi-Box Plot",
            "file": "chart-4-by-rep-distribution.html"
        },
        {
            "id": "2.x",
            "title": "Rep-Level Boxplots",
            "desc": "Alternative view of per-rep distributions sorted by median performance",
            "tag": "Multi-Box Plot",
            "file": "chart-view2-by-rep-boxplots.html"
        }
    ],
    "View 2.3-2.4: Prospecting by Account Tier": [
        {
            "id": "2.3",
            "title": "Tier 1 Prospecting",
            "desc": "Distribution of SQLs from prospecting against Tier 1 accounts per ramped rep per month",
            "tag": "Box + Strip Plot",
            "file": "chart-5-t1-prospecting.html"
        },
        {
            "id": "2.4",
            "title": "Non-Tier 1 Prospecting",
            "desc": "Distribution of SQLs from prospecting against non-Tier 1 accounts per ramped rep per month",
            "tag": "Box + Strip Plot",
            "file": "chart-6-non-t1-prospecting.html"
        },
        {
            "id": "T1",
            "title": "Tier 1 vs Non-Tier 1 by Month",
            "desc": "Monthly comparison of T1 vs non-T1 SQL volume across all sources",
            "tag": "Stacked Bar",
            "file": "chart-t1-by-month.html"
        },
        {
            "id": "T1",
            "title": "Tier 1 vs Non-Tier 1 per Rep",
            "desc": "Per-rep breakdown of T1 vs non-T1 SQLs for the year",
            "tag": "Stacked Bar",
            "file": "chart-t1-per-rep.html"
        }
    ],
    "View 2.5-2.8: By Source Type": [
        {
            "id": "2.5",
            "title": "Conference Distribution",
            "desc": "Distribution of Conference SQLs per rep per conference event",
            "tag": "Box + Strip Plot",
            "file": "chart-7-conference-distribution.html"
        },
        {
            "id": "2.7",
            "title": "Demo Request (Inbound)",
            "desc": "Monthly team total of inbound Demo Request SQLs - marketing-driven baseline",
            "tag": "Box + Strip Plot",
            "file": "chart-9-demo-request.html"
        },
        {
            "id": "2.8",
            "title": "Referrals",
            "desc": "Monthly team total of Referral SQLs - highest conversion rate (34.5%)",
            "tag": "Box + Strip Plot",
            "file": "chart-10-referrals.html"
        }
    ]
}

# Get charts directory
CHARTS_DIR = Path(__file__).parent / "charts"

def load_chart_html(filename):
    """Load HTML content from chart file"""
    filepath = CHARTS_DIR / filename
    if filepath.exists():
        content = filepath.read_text()
        # Remove the back navigation header (Streamlit has its own)
        if 'Back to Dashboard' in content:
            start = content.find('<div style="font-family: Inter')
            if start != -1:
                end = content.find('</div>', start) + 6
                content = content[:start] + content[end:]
        return content
    return f"<p>Chart not found: {filename}</p>"

# Initialize session state
if 'current_chart' not in st.session_state:
    st.session_state.current_chart = None

def show_homepage():
    """Display the card-based navigation homepage"""
    st.title("📊 RevStaff Full Funnel Metrics")
    st.caption("2025 Performance Analysis | Data through Dec 29, 2025 | n=416 SQLs")

    for section_name, charts in SECTIONS.items():
        st.markdown(f"#### {section_name}")

        # Create columns for cards
        num_charts = len(charts)
        cols = st.columns(min(num_charts, 3))

        for i, chart in enumerate(charts):
            with cols[i % 3]:
                # Create a card-like container
                with st.container(border=True):
                    st.markdown(f"**{chart['id']} {chart['title']}**")
                    st.caption(chart['desc'])
                    st.markdown(f"`{chart['tag']}`")
                    if st.button("View →", key=chart['file'], use_container_width=True):
                        st.session_state.current_chart = chart
                        st.rerun()

        st.markdown("")  # Spacing between sections

def show_chart(chart):
    """Display a single chart with back navigation"""
    # Back button
    col1, col2 = st.columns([1, 11])
    with col1:
        if st.button("← Back"):
            st.session_state.current_chart = None
            st.rerun()

    # Header
    st.markdown(f"### {chart['id']} {chart['title']}")
    st.caption(chart['desc'])

    # Load and display chart
    html_content = load_chart_html(chart['file'])
    st.components.v1.html(html_content, height=650, scrolling=True)

# Main app logic
if st.session_state.current_chart is None:
    show_homepage()
else:
    show_chart(st.session_state.current_chart)

# Footer
st.divider()
st.caption("RevStaff Full Funnel Metrics | HubSpot export Dec 29, 2025 | Cohort Month methodology")
