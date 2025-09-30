import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import random
from datetime import datetime, timedelta
import json
import base64

# Configure page
st.set_page_config(
    page_title="Data, AI, and PAL - Now and Future",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS matching RPAG design
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #4DD0E1 0%, #26C6DA 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }

    .pain-point-card {
        background: linear-gradient(135deg, #FF7043 0%, #E91E63 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }

    .solution-card {
        background: linear-gradient(135deg, #4DD0E1 0%, #1E3A8A 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }

    .metric-card {
        background: rgba(255,255,255,0.04);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #FF7043;
        box-shadow: 0 2px 8px rgba(0,0,0,0.5);
        color: #e5e7eb;
    }

    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #4DD0E1 0%, #26C6DA 100%);
    }

    /* Top spacing without constraining width */
    div.block-container { padding-top: 1rem; }

    /* Sleek top navigation container */
    .top-nav {
        position: sticky;
        top: 0;
        z-index: 50;
        background: rgba(15, 23, 42, 0.75);
        -webkit-backdrop-filter: saturate(180%) blur(12px);
        backdrop-filter: saturate(180%) blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 12px;
        padding: 0.5rem 0.75rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        color: #e5e7eb;
    }

    /* Center and expand segmented control */
    [data-testid="stSegmentedControl"] {
        width: 100%;
    }

    [data-testid="stSegmentedControl"] > div {
        justify-content: center;
    }

    /* Make segment pills rounded and modern */
    [data-testid="stSegmentedControl"] button {
        border-radius: 999px !important;
        padding: 0.5rem 1rem !important;
    }

    /* Comparison cards for Before vs After */
    .compare-wrapper {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .compare-card {
        border-radius: 12px;
        color: #fff;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    }
    .compare-card.current {
        background: linear-gradient(135deg, #FF7043 0%, #E91E63 100%);
    }
    .compare-card.future {
        background: linear-gradient(135deg, #4DD0E1 0%, #1E3A8A 100%);
    }
    .compare-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin: 0 0 .5rem 0;
    }
    .compare-divider {
        height: 1px;
        background: rgba(255,255,255,0.25);
        margin: .5rem 0 1rem;
    }
    .compare-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: .75rem;
        padding: .4rem 0;
    }
    .compare-label { opacity: .95; }
    .compare-value { font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# Title with RPAG branding (logo embedded)
logo_img_tag = ""
try:
    with open("rpaglogo.jpg", "rb") as _logo_f:
        _logo_b64 = base64.b64encode(_logo_f.read()).decode()
        logo_img_tag = f'<img src="data:image/jpeg;base64,{_logo_b64}" alt="RPAG Logo" style="height:60px;margin-bottom:12px;border-radius:6px;" />'
except Exception:
    pass

header_html = f"""
<div class=\"main-header\">{logo_img_tag}
    <h1>Data, AI, and PAL</h1>
    <h2>Now and in The Future</h2>
    <p style=\"font-size: 1.2em; opacity: 0.9;\">Powering Your Growth Through Innovation</p>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# Initialize session state
if 'demo_stage' not in st.session_state:
    st.session_state.demo_stage = 'intro'
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'demo_nav' not in st.session_state:
    st.session_state.demo_nav = st.session_state.demo_stage

# Demo navigation
demo_stages = {
    'intro': "The Challenge: Current PAL Pain Points",
    'pre_ingestion': "AI-Powered Pre-Ingestion Intelligence",
    'post_ingestion': "Process Automation: Post-Ingestion",
    'future': "Building Your Data Backbone"
}

# Sleek top navigation (with safe sidebar fallback)
demo_stage_labels = {
    'intro': 'Challenge',
    'pre_ingestion': 'Pre-Ingestion',
    'post_ingestion': 'Post-Ingestion',
    'future': 'Future'
}

with st.container():
    st.markdown('<div class="top-nav">', unsafe_allow_html=True)
    if hasattr(st, "segmented_control"):
        selected_stage = st.segmented_control(
            "",
            options=list(demo_stages.keys()),
            format_func=lambda x: demo_stage_labels.get(x, x),
            key="demo_nav"
        )
    else:
        st.sidebar.title("Navigation")
        selected_stage = st.sidebar.radio(
            "Choose Demo Section:",
            list(demo_stages.keys()),
            format_func=lambda x: demo_stages[x],
            key="demo_nav"
        )
    st.markdown('</div>', unsafe_allow_html=True)

st.session_state.demo_stage = selected_stage

# Generate mock PAL data
@st.cache_data
def generate_mock_pal_data():
    """Generate realistic mock PAL data with various quality issues"""

    # Provider templates with different formats/issues
    providers = [
        {"name": "Fidelity", "template_type": "CSV", "issues": ["Missing Contract Numbers", "Inconsistent Date Formats"]},
        {"name": "Vanguard", "template_type": "Excel", "issues": ["Extra Header Rows", "Merged Cells"]},
        {"name": "T. Rowe Price", "template_type": "XML", "issues": ["Special Characters", "Encoding Issues"]},
        {"name": "Principal", "template_type": "CSV", "issues": ["Fund Name Variations", "Decimal Precision"]},
        {"name": "Empower", "template_type": "Excel", "issues": ["Multiple Worksheets", "Formula References"]},
        {"name": "John Hancock", "template_type": "Fixed Width", "issues": ["No Delimiters", "Padding Spaces"]},
        {"name": "Mass Mutual", "template_type": "JSON", "issues": ["Nested Objects", "Missing Fields"]},
        {"name": "TIAA", "template_type": "XML", "issues": ["Namespace Issues", "Invalid Characters"]}
    ]

    # Generate plan data with issues
    plans_data = []
    for i in range(50):
        provider = random.choice(providers)

        # Contract number issues
        if "Missing Contract Numbers" in provider["issues"]:
            contract_no = "" if random.random() < 0.3 else f"CNT-{random.randint(10000, 99999)}"
        else:
            contract_no = f"CNT-{random.randint(10000, 99999)}"

        # Plan name variations
        plan_names = [
            "ABC Corp 401(k) Plan",
            "ABC CORP 401K PLAN",
            "ABC Corporation Retirement Plan",
            "ABC Co. 401(k)"
        ]

        plans_data.append({
            "provider": provider["name"],
            "template_type": provider["template_type"],
            "contract_number": contract_no,
            "plan_name": random.choice(plan_names) if random.random() > 0.2 else "ABC Corp 401(k) Plan",
            "client_name": f"Company {chr(65 + i % 26)}{chr(65 + (i//26) % 26)}",
            "assets": random.randint(500000, 50000000),
            "participants": random.randint(25, 2500),
            "last_updated": datetime.now() - timedelta(days=random.randint(1, 90)),
            "data_quality_score": random.randint(45, 95),
            "issues": provider["issues"],
            "processing_time_hours": round(random.uniform(0.5, 8.0), 1)
        })

    return pd.DataFrame(plans_data)

# Generate fund mapping data
@st.cache_data
def generate_fund_mapping_data():
    """Generate fund mapping data with mismatches"""

    funds_data = []
    fund_families = ["American Funds", "Vanguard", "Fidelity", "T. Rowe Price", "BlackRock"]

    for i in range(100):
        family = random.choice(fund_families)

        # Fund name variations that need mapping
        base_name = f"{family} Growth Fund"
        variations = [
            base_name,
            f"{family} Growth Fd",
            f"{family.upper()} GROWTH FUND",
            f"{family} Growth Portfolio",
            f"{family} Growth Fund Class A"
        ]

        funds_data.append({
            "pal_fund_name": random.choice(variations),
            "master_fund_name": base_name,
            "ticker": f"A{family[0]}{random.randint(100, 999)}X",
            "match_confidence": random.uniform(0.3, 0.99),
            "requires_review": random.random() < 0.4,
            "asset_value": random.randint(10000, 5000000)
        })

    return pd.DataFrame(funds_data)

# Main demo content
if st.session_state.demo_stage == 'intro':
    # Load mock data
    pal_data = generate_mock_pal_data()

    tabs = st.tabs(["Overview", "Challenges", "Scenarios"])

    with tabs[0]:
        st.markdown("""
        <div class="pain-point-card">
            <h2>The Real PAL Challenges</h2>
            <p><em>"We allocate multiple hours to get through our quarterly data, and that's just the beginning..."</em></p>
            <p>- RPAG Member Survey Response</p>
        </div>
        """, unsafe_allow_html=True)

        # KPI metrics
        col_kpi_1, col_kpi_2, col_kpi_3 = st.columns(3)
        total_templates = len(pal_data['template_type'].unique()) * 50  # Simulate 400+ templates
        avg_processing_time = pal_data['processing_time_hours'].mean()
        low_quality_pct = (pal_data['data_quality_score'] < 70).mean() * 100

        with col_kpi_1:
            st.metric("Total PAL Templates", f"{total_templates}+")
        with col_kpi_2:
            st.metric("Avg Processing Time", f"{avg_processing_time:.1f} hours")
        with col_kpi_3:
            st.metric("Data Quality Issues", f"{low_quality_pct:.0f}%")

        col_a, col_b = st.columns(2)
        with col_a:
            fig_time = px.histogram(
                pal_data,
                x='processing_time_hours',
                title="PAL Processing Time Distribution",
                color_discrete_sequence=['#FF7043']
            )
            fig_time.update_layout(
                xaxis_title="Hours to Process",
                yaxis_title="Number of Plans"
            )
            st.plotly_chart(fig_time, use_container_width=True)

        with col_b:
            fig_quality_dist = px.histogram(
                pal_data,
                x='data_quality_score',
                title="Data Quality Score Distribution",
                color_discrete_sequence=['#26C6DA'],
                nbins=20
            )
            fig_quality_dist.update_layout(
                xaxis_title="Quality Score",
                yaxis_title="Number of Plans"
            )
            st.plotly_chart(fig_quality_dist, use_container_width=True)

    with tabs[1]:
        st.subheader("Real-World PAL Challenges")
        real_pain_points = [
            "Manual first-time setup (30+ plans)",
            "Silent feed disconnections",
            "Complex fund lineups (100+ funds)",
            "No rollback capability",
            "Provider data inconsistencies",
            "Quarterly sync confusion",
            "Missing error notifications",
            "Blended fund lineups"
        ]

        pain_points_data = pd.DataFrame({
            'Challenge': real_pain_points,
            'Impact_Score': [9, 8, 7, 8, 9, 6, 7, 6],
            'Frequency': ['High', 'Medium', 'High', 'Medium', 'High', 'Low', 'Medium', 'Medium']
        })

        col_left, col_right = st.columns(2)
        with col_left:
            st.dataframe(pain_points_data, use_container_width=True)

            fig_challenges = px.bar(
                pain_points_data,
                x='Impact_Score',
                y='Challenge',
                orientation='h',
                color='Impact_Score',
                title="Challenge Impact",
                color_continuous_scale=['#FF7043', '#E91E63', '#C2185B']
            )
            fig_challenges.update_layout(
                xaxis_title="Impact Score (1-10)",
                yaxis_title="Challenge Type",
                height=400
            )
            st.plotly_chart(fig_challenges, use_container_width=True)

        with col_right:
            provider_issues = pd.DataFrame({
                'Provider': ['Provider A', 'Provider B', 'Provider C', 'Provider D', 'Provider E', 'Provider F'],
                'Data_Quality_Score': [45, 52, 78, 85, 92, 88],
                'Common_Issues': [
                    'Incomplete feeds, complex lineups',
                    'Blended fund data, poor differentiation', 
                    'Format inconsistencies',
                    'Missing contract numbers',
                    'Standard format, reliable',
                    'Minor formatting issues'
                ]
            })

            fig_quality = px.bar(
                provider_issues,
                x='Data_Quality_Score',
                y='Provider',
                orientation='h',
                color='Data_Quality_Score',
                title="Data Quality by Provider (Anonymized)",
                color_continuous_scale=['#FF7043', '#FFA726', '#FFC107', '#8BC34A', '#4CAF50']
            )
            fig_quality.update_layout(
                xaxis_title="Data Quality Score",
                yaxis_title="Provider",
                height=300
            )
            st.plotly_chart(fig_quality, use_container_width=True)

    with tabs[2]:
        st.subheader("Real-World Problematic Scenarios")
        problematic_scenarios = pd.DataFrame({
            'Scenario': [
                'Complex Fund Lineup',
                'Silent Feed Disconnection', 
                'Blended Fund Data',
                'Missing Contract Numbers',
                'Quarterly Sync Confusion',
                'Manual Setup Required'
            ],
            'Impact': [
                '100+ funds, old funds included',
                'No notification, 2-month delay',
                'Cannot differentiate fund sources',
                'Manual entry required',
                'Premature saves, manual corrections',
                '30+ plans need individual review'
            ],
            'Current_Resolution': [
                'Manual fund mapping',
                'Submit support ticket',
                'Manual data separation',
                'Manual contract lookup',
                'Manual value corrections',
                'One-by-one plan review'
            ],
            'Time_Impact': [
                '4-6 hours',
                '2+ months',
                '2-3 hours',
                '30-60 minutes',
                '1-2 hours',
                '2-3 days'
            ]
        })

        st.dataframe(problematic_scenarios, use_container_width=True)

elif st.session_state.demo_stage == 'pre_ingestion':
    st.markdown("""
    <div class="solution-card">
        <h2>AI-Powered Pre-Ingestion Intelligence</h2>
        <p>Transform 400+ chaotic templates into clean, standardized data</p>
    </div>
    """, unsafe_allow_html=True)

    # API Migration Focus
    st.subheader("The Future of Data Ingestion: From Files to APIs")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>Current State: File-Based Processing</h4>
            <ul>
                <li>Manual file uploads</li>
                <li>Batch processing delays</li>
                <li>Format inconsistencies</li>
                <li>Error-prone transfers</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="solution-card" style="margin-top: 1rem;">
            <h4>Future State: Real-Time API Integration</h4>
            <ul>
                <li>Instant data synchronization</li>
                <li>Real-time updates</li>
                <li>Standardized data formats</li>
                <li>Automated error handling</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # API connection simulation
        st.markdown("#### API Connection Status")
        
        api_status = st.selectbox(
            "Select Provider API Status:",
            ["Fidelity API v2.1", "Vanguard REST API v3.4", "T. Rowe Price GraphQL v1.8", "Legacy File Upload"],
            help="Choose a provider to see their API integration status"
        )
        
        if "Legacy File Upload" in api_status:
            st.error("⚠️ File-based processing - Consider API migration")
        else:
            st.success("✅ API-enabled - Real-time data available")

        demo_mode = st.button("Simulate API Data Flow", type="primary")

        if demo_mode:
            # Simulate API-based processing
            with st.spinner("API Data Synchronization Running..."):
                progress_bar = st.progress(0)
                status_text = st.empty()

                if "Legacy File Upload" in api_status:
                    steps = [
                        "Uploading files to server...",
                        "Detecting file format...",
                        "Analyzing template structure...",
                        "AI template matching (400+ templates)...",
                        "Smart field mapping...",
                        "Data standardization...",
                        "Quality validation...",
                        "Generating insights..."
                    ]
                else:
                    steps = [
                        "Establishing API connection...",
                        "Authenticating with provider...",
                        "Fetching real-time data...",
                        "Validating data schema...",
                        "Applying AI transformations...",
                        "Synchronizing with master database...",
                        "Generating live insights..."
                    ]

                for i, step in enumerate(steps):
                    status_text.text(step)
                    progress_bar.progress((i + 1) / len(steps))
                    time.sleep(0.8)

                if "Legacy File Upload" in api_status:
                    st.success("File Processing Complete!")
                else:
                    st.success("API Synchronization Complete!")

    with col2:
        if demo_mode or st.session_state.get('ai_processed'):
            st.session_state.ai_processed = True

            # API vs File Processing Results
            st.subheader("API vs File Processing Results")

            # Metrics comparison
            col_a, col_b, col_c, col_d = st.columns(4)

            if "Legacy File Upload" in api_status:
                with col_a:
                    st.metric("Data Freshness", "24-48 hours", "Batch delay")
                with col_b:
                    st.metric("Processing Time", "12 min", "Per file")
                with col_c:
                    st.metric("Error Rate", "8.2%", "Manual fixes")
                with col_d:
                    st.metric("Sync Frequency", "Daily", "Scheduled")
            else:
                with col_a:
                    st.metric("Data Freshness", "Real-time", "Live updates")
                with col_b:
                    st.metric("Processing Time", "2 min", "Per sync")
                with col_c:
                    st.metric("Error Rate", "1.1%", "Auto-resolved")
                with col_d:
                    st.metric("Sync Frequency", "Continuous", "On-demand")

            # Data source results
            if "Legacy File Upload" in api_status:
                st.subheader("File Processing Analysis")
                template_results = pd.DataFrame({
                    'File': ['Fidelity_Q3_2024.csv', 'Vanguard_Sept.xlsx', 'TRP_Quarterly.xml'],
                    'Detected Template': ['Fidelity Standard v2.1', 'Vanguard Institutional v3.4', 'T.Rowe Price XML v1.8'],
                    'Confidence': [99.2, 97.8, 94.1],
                    'Issues Found': [2, 5, 12],
                    'Auto-Fixed': [2, 4, 10]
                })
            else:
                st.subheader("API Data Integration")
                template_results = pd.DataFrame({
                    'Provider': ['Fidelity API v2.1', 'Vanguard REST API v3.4', 'T.Rowe Price GraphQL v1.8'],
                    'Data Schema': ['Standardized JSON', 'RESTful JSON', 'GraphQL Schema'],
                    'Sync Status': ['Live', 'Live', 'Live'],
                    'Last Update': ['2 min ago', '30 sec ago', '1 min ago'],
                    'Data Quality': [99.8, 99.5, 99.2]
                })

            # Color code based on mode
            if "Legacy File Upload" in api_status:
                def color_confidence(val):
                    if val > 95:
                        return 'background-color: #d4edda'
                    elif val > 85:
                        return 'background-color: #fff3cd'
                    else:
                        return 'background-color: #f8d7da'

                st.dataframe(
                    template_results.style.applymap(color_confidence, subset=['Confidence']),
                    use_container_width=True
                )
            else:
                def color_status(val):
                    # Dark-friendly tints with readable text
                    if val == 'Live':
                        return 'background-color: rgba(16,185,129,0.22); color: #e5e7eb;'
                    else:
                        return 'background-color: rgba(239,68,68,0.22); color: #e5e7eb;'

                st.dataframe(
                    template_results.style.applymap(color_status, subset=['Sync Status']),
                    use_container_width=True
                )

            # Data transformation visualization
            if "Legacy File Upload" in api_status:
                st.subheader("File-Based Field Mapping")
                mapping_data = {
                    'PAL Field': ['CONT_NUM', 'PLN_NM', 'AST_VAL', 'PARTIC_CNT', 'DT_ASOF'],
                    'Standard Field': ['Contract_Number', 'Plan_Name', 'Asset_Value', 'Participant_Count', 'As_Of_Date'],
                    'Confidence': [99.8, 94.2, 99.9, 98.1, 87.3],
                    'Transformation': ['Direct Map', 'Text Clean', 'Currency Parse', 'Number Parse', 'Date Standard']
                }
            else:
                st.subheader("API Data Standardization")
                mapping_data = {
                    'API Field': ['contractNumber', 'planName', 'assetValue', 'participantCount', 'asOfDate'],
                    'Standard Field': ['Contract_Number', 'Plan_Name', 'Asset_Value', 'Participant_Count', 'As_Of_Date'],
                    'Mapping Type': ['Direct', 'Direct', 'Direct', 'Direct', 'Direct'],
                    'Validation': ['Schema Validated', 'Schema Validated', 'Schema Validated', 'Schema Validated', 'Schema Validated']
                }

            mapping_df = pd.DataFrame(mapping_data)

            if "Legacy File Upload" in api_status:
                fig_mapping = px.bar(
                    mapping_df,
                    x='PAL Field',
                    y='Confidence',
                    color='Confidence',
                    title="File-Based Field Mapping Confidence Scores",
                    color_continuous_scale=['#FF7043', '#4DD0E1', '#26C6DA']
                )
                fig_mapping.update_layout(yaxis_title="Confidence %")
            else:
                fig_mapping = px.bar(
                    mapping_df,
                    x='API Field',
                    y=[100, 100, 100, 100, 100],  # API fields have 100% reliability
                    color=[100, 100, 100, 100, 100],
                    title="API Data Standardization Reliability",
                    color_continuous_scale=['#4DD0E1', '#26C6DA', '#1E3A8A']
                )
                fig_mapping.update_layout(yaxis_title="Reliability %")
            
            st.plotly_chart(fig_mapping, use_container_width=True)

            # API Migration Benefits Summary
            st.markdown("---")
            st.subheader("Why Move to APIs?")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div class="metric-card">
                    <h4>Immediate Benefits</h4>
                    <ul>
                        <li>Real-time data access</li>
                        <li>Eliminate file transfers</li>
                        <li>Reduce manual errors</li>
                        <li>Faster processing</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="metric-card">
                    <h4>Operational Impact</h4>
                    <ul>
                        <li>85% reduction in processing time</li>
                        <li>99% data accuracy</li>
                        <li>24/7 data availability</li>
                        <li>Automated error handling</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="metric-card">
                    <h4>Strategic Value</h4>
                    <ul>
                        <li>Enhanced client experience</li>
                        <li>Competitive advantage</li>
                        <li>Scalable architecture</li>
                        <li>Future-proof solution</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

elif st.session_state.demo_stage == 'post_ingestion':
    st.markdown("""
    <div class="solution-card">
        <h2>Process Automation: Post-Ingestion</h2>
        <p>Intelligent workflows that minimize manual intervention</p>
    </div>
    """, unsafe_allow_html=True)

    # Plan matching demo
    st.subheader("AI-Powered Plan Matching")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Incoming PAL Plans")

        incoming_plans = pd.DataFrame({
            'Contract_Number': ['CNT-45289', '', 'CNT-78934', 'CNT-12456'],
            'Plan_Name': ['ABC Corp 401K Plan', 'XYZ Company Retirement', 'DEF Inc 401(k) Plan', 'GHI Corp Plan'],
            'Client_Name': ['ABC Corporation', 'XYZ Company LLC', 'DEF Industries', 'GHI Corp'],
            'Assets': ['$2.5M', '$890K', '$5.2M', '$1.8M']
        })

        st.dataframe(incoming_plans, use_container_width=True)

        if st.button("Run AI Matching", type="primary"):
            with st.spinner("AI analyzing plan relationships..."):
                time.sleep(2)
                st.session_state.matching_complete = True
                st.success("Matching complete!")

    with col2:
        st.markdown("#### AI Matching Results")

        if st.session_state.get('matching_complete'):
            matching_results = pd.DataFrame({
                'PAL Plan': ['ABC Corp 401K Plan', 'XYZ Company Retirement', 'DEF Inc 401(k) Plan', 'GHI Corp Plan'],
                'Matched Plan': ['ABC Corp 401(k)', 'XYZ Co. Retirement Plan', 'DEF Industries 401(k)', 'New Plan'],
                'Confidence': [94.8, 87.2, 99.1, 0.0],
                'Action': ['Auto-Sync', 'Review Required', 'Auto-Sync', 'Manual Setup']
            })

            # Color code by confidence (dark-friendly)
            def color_matching(row):
                if row['Confidence'] > 90:
                    bg = 'rgba(16,185,129,0.18)'
                elif row['Confidence'] > 80:
                    bg = 'rgba(234,179,8,0.20)'
                else:
                    bg = 'rgba(239,68,68,0.20)'
                return [f'background-color: {bg}; color: #e5e7eb;'] * len(row)

            st.dataframe(
                matching_results.style.apply(color_matching, axis=1),
                use_container_width=True
            )
        else:
            st.info("Run AI matching to see results")

    # Fund Association Intelligence
    st.subheader("Smart Fund Association")

    fund_data = generate_fund_mapping_data()

    col1, col2 = st.columns(2)

    with col1:
        # Show fund matching confidence
        fig_confidence = px.histogram(
            fund_data,
            x='match_confidence',
            title="Fund Matching Confidence Distribution",
            color_discrete_sequence=['#4DD0E1'],
            nbins=20
        )
        fig_confidence.update_layout(
            xaxis_title="Match Confidence",
            yaxis_title="Number of Funds"
        )
        st.plotly_chart(fig_confidence, use_container_width=True)

        # High confidence matches - show 92/100 auto-matched
        auto_matched_count = 92  # Fixed number for consistency
        st.metric("Auto-Matched Funds", f"{auto_matched_count}/{len(fund_data)}", "88%")

    with col2:
        # Show funds requiring review
        st.markdown("#### Funds Requiring Review")

        review_funds = fund_data[fund_data['requires_review']].head(8)

        st.dataframe(
            review_funds[['pal_fund_name', 'master_fund_name', 'match_confidence', 'ticker']],
            use_container_width=True
        )

        st.info(f"AI reduced manual review from 100 to 8 funds (92% reduction)")

    # Feed Management Intelligence
    st.subheader("Feed Management Intelligence")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Real-Time Feed Monitoring")
        
        # Feed status dashboard
        feed_status = pd.DataFrame({
            'Plan': ['ABC Corp 401(k)', 'XYZ Company Plan', 'DEF Industries', 'GHI Corp Plan'],
            'Provider': ['Provider A', 'Provider B', 'Provider C', 'Provider D'],
            'Status': ['Connected', 'Disconnected', 'Connected', 'Warning'],
            'Last_Sync': ['2 min ago', '2 days ago', '5 min ago', '1 hour ago'],
            'Data_Quality': ['99.2%', 'N/A', '98.8%', '87.3%']
        })

        # Color code by status (dark-friendly)
        def color_feed_status(val):
            if val == 'Connected':
                return 'background-color: rgba(16,185,129,0.20); color: #e5e7eb;'
            elif val == 'Disconnected':
                return 'background-color: rgba(239,68,68,0.22); color: #e5e7eb;'
            elif val == 'Warning':
                return 'background-color: rgba(234,179,8,0.22); color: #0b0b0b;'
            else:
                return ''

        st.dataframe(
            feed_status.style.applymap(color_feed_status, subset=['Status']),
            use_container_width=True
        )

        # AI-powered alerts
        st.markdown("#### AI-Powered Alerts")
        st.success("✅ Feed disconnection detected for XYZ Company Plan")
        st.warning("⚠️ Data quality drop detected for GHI Corp Plan")
        st.info("ℹ️ New fund detected in ABC Corp 401(k)")

    with col2:
        st.markdown("#### One-Click Problem Resolution")
        
        # Resolution actions
        resolution_actions = pd.DataFrame({
            'Issue': [
                'Feed Disconnection',
                'Data Quality Drop',
                'Missing Contract Numbers',
                'Complex Fund Lineup',
                'Quarterly Sync Error'
            ],
            'AI_Action': [
                'Auto-reconnect + notify',
                'Auto-correct + flag for review',
                'Auto-lookup from provider',
                'Auto-map + confidence score',
                'Auto-rollback + resync'
            ],
            'Time_Saved': [
                '2+ months',
                '2-3 hours',
                '30-60 minutes',
                '4-6 hours',
                '1-2 hours'
            ]
        })

        st.dataframe(resolution_actions, use_container_width=True)

        # Rollback capability demo
        st.markdown("#### Smart Rollback Capability")
        if st.button("Demo: Rollback to Previous Quarter", type="primary"):
            with st.spinner("AI analyzing historical data..."):
                time.sleep(2)
                st.success("✅ Successfully rolled back to Q3 2024 data")
                st.info("All 47 plans restored to previous quarter values")

    # Exception handling with AI insights
    st.subheader("Intelligent Exception Handling")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>Silent Disconnection Detection</h4>
            <p>AI automatically detected and resolved:</p>
            <ul>
                <li>3 silent feed disconnections</li>
                <li>2 data quality drops</li>
                <li>1 missing contract number</li>
                <li>Auto-notifications sent to advisors</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>Complex Fund Lineup Management</h4>
            <p>AI intelligently handled:</p>
            <ul>
                <li>100+ fund complex lineups</li>
                <li>Blended fund data separation</li>
                <li>Old fund identification & mapping</li>
                <li>Confidence scoring for each fund</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>Smart Rollback & Recovery</h4>
            <p>AI automatically managed:</p>
            <ul>
                <li>Quarterly sync error prevention</li>
                <li>One-click rollback to previous data</li>
                <li>Manual correction elimination</li>
                <li>Historical data preservation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

else:  # future stage
    st.markdown("""
    <div class="solution-card">
        <h2>Building Your Data Backbone</h2>
        <p>The Future of PAL Processing at RPAG</p>
    </div>
    """, unsafe_allow_html=True)

    # ROI Comparison
    st.subheader("The Transformation: Before vs After AI")

    st.markdown(
        """
        <div class="compare-wrapper">
            <div class="compare-card current">
                <div class="compare-title">Current State (Manual Process)</div>
                <div class="compare-divider"></div>
                <div class="compare-item"><span class="compare-label">Processing Time</span><span class="compare-value">6.5 hours avg</span></div>
                <div class="compare-item"><span class="compare-label">Data Quality Score</span><span class="compare-value">68%</span></div>
                <div class="compare-item"><span class="compare-label">Manual Review Required</span><span class="compare-value">89%</span></div>
                <div class="compare-item"><span class="compare-label">Exception Resolution</span><span class="compare-value">2.3 hours avg</span></div>
                <div class="compare-item"><span class="compare-label">Quarterly Processing</span><span class="compare-value">2-3 business days</span></div>
            </div>
            <div class="compare-card future">
                <div class="compare-title">AI-Powered Future</div>
                <div class="compare-divider"></div>
                <div class="compare-item"><span class="compare-label">Processing Time</span><span class="compare-value">15 minutes avg</span></div>
                <div class="compare-item"><span class="compare-label">Data Quality Score</span><span class="compare-value">94%</span></div>
                <div class="compare-item"><span class="compare-label">Manual Review Required</span><span class="compare-value">12%</span></div>
                <div class="compare-item"><span class="compare-label">Exception Resolution</span><span class="compare-value">5 minutes avg</span></div>
                <div class="compare-item"><span class="compare-label">Quarterly Processing</span><span class="compare-value">2 hours</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Visual impact
    st.subheader("Impact Visualization")

    # Time savings chart
    categories = ['Data Processing', 'Plan Matching', 'Fund Mapping', 'Exception Handling', 'Quality Review']
    current_times = [6.5, 2.1, 3.2, 2.3, 1.8]
    ai_times = [0.25, 0.1, 0.3, 0.08, 0.2]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Current Manual Process',
        x=categories,
        y=current_times,
        marker_color='#FF7043'
    ))

    fig.add_trace(go.Bar(
        name='AI-Powered Future',
        x=categories,
        y=ai_times,
        marker_color='#4DD0E1'
    ))

    fig.update_layout(
        title='Processing Time: Current vs AI-Powered Future',
        xaxis_title='Process Category',
        yaxis_title='Hours',
        barmode='group'
    )

    st.plotly_chart(fig, use_container_width=True)


    # Call to action
    st.markdown("""
    <div class="solution-card">
        <h3>The Power to GROW</h3>
        <p style="font-size: 1.1em;">
        From <strong>hours to minutes</strong>. From <strong>manual to intelligent</strong>.
        From <strong>reactive to predictive</strong>.
        </p>
        <p style="font-size: 1.1em;">
        This is how we build the retirement industry's data backbone -
        enabling faster, smarter, and more connected decisions across all stakeholders.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Final metrics summary
    st.subheader("Summary: Empowering the Automation Advocates")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Time Savings", "5.5 hours", "per quarterly review")
    with col2:
        st.metric("Quality Improvement", "+26 points", "data quality score")
    with col3:
        st.metric("Manual Work Reduction", "-77%", "review requirements")
    with col4:
        st.metric("Processing Speed", "26x faster", "end-to-end")

# Demo controls
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:

    st.markdown(f"<center><strong>{demo_stages[selected_stage]}</strong></center>", unsafe_allow_html=True)
