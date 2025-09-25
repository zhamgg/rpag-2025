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

# Configure page
st.set_page_config(
    page_title="Data, AI, and PAL - Now and Future at RPAG",
    page_icon="🚀",
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
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #FF7043;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #4DD0E1 0%, #26C6DA 100%);
    }
</style>
""", unsafe_allow_html=True)

# Title with RPAG branding
st.markdown("""
<div class="main-header">
    <h1>🚀 Data, AI, and PAL</h1>
    <h2>Now and in The Future at RPAG</h2>
    <p style="font-size: 1.2em; opacity: 0.9;">Powering Your Growth Through Innovation</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'demo_stage' not in st.session_state:
    st.session_state.demo_stage = 'intro'
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None

# Demo navigation
demo_stages = {
    'intro': "📊 The Challenge: Current PAL Pain Points",
    'pre_ingestion': "🤖 AI-Powered Pre-Ingestion Intelligence",
    'post_ingestion': "⚡ Process Automation: Post-Ingestion",
    'future': "🌟 Building Your Data Backbone"
}

# Sidebar navigation
st.sidebar.title("Demo Navigation")
selected_stage = st.sidebar.radio(
    "Choose Demo Section:",
    list(demo_stages.keys()),
    format_func=lambda x: demo_stages[x],
    key="demo_nav"
)

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
    st.markdown("""
    <div class="pain-point-card">
        <h2>🎯 The Automation Advocates' Challenge</h2>
        <p><em>"We allocate multiple hours to get through our quarterly data."</em></p>
        <p>- RPAG Member Survey Response</p>
    </div>
    """, unsafe_allow_html=True)

    # Load mock data
    pal_data = generate_mock_pal_data()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Current PAL Processing Reality")

        # Key metrics
        total_templates = len(pal_data['template_type'].unique()) * 50  # Simulate 400+ templates
        avg_processing_time = pal_data['processing_time_hours'].mean()
        low_quality_pct = (pal_data['data_quality_score'] < 70).mean() * 100

        st.metric("Total PAL Templates", f"{total_templates}+")
        st.metric("Avg Processing Time", f"{avg_processing_time:.1f} hours")
        st.metric("Data Quality Issues", f"{low_quality_pct:.0f}%")

        # Processing time distribution
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

    with col2:
        st.subheader("🚨 Top Data Pain Points")

        # Issue frequency analysis
        all_issues = []
        for issues in pal_data['issues']:
            all_issues.extend(issues)

        issue_counts = pd.Series(all_issues).value_counts()

        fig_issues = px.bar(
            x=issue_counts.values,
            y=issue_counts.index,
            orientation='h',
            title="Most Common Data Issues",
            color_discrete_sequence=['#E91E63']
        )
        fig_issues.update_layout(
            xaxis_title="Frequency",
            yaxis_title="Issue Type"
        )
        st.plotly_chart(fig_issues, use_container_width=True)

        # Data quality by provider
        quality_by_provider = pal_data.groupby('provider')['data_quality_score'].mean().sort_values()

        fig_quality = px.bar(
            x=quality_by_provider.values,
            y=quality_by_provider.index,
            orientation='h',
            title="Data Quality Score by Provider",
            color_discrete_sequence=['#FF7043']
        )
        fig_quality.update_layout(
            xaxis_title="Average Quality Score",
            yaxis_title="Provider"
        )
        st.plotly_chart(fig_quality, use_container_width=True)

    # Show sample problematic data
    st.subheader("📋 Sample Problematic PAL Data")

    # Filter to show problematic records
    problematic_data = pal_data[pal_data['data_quality_score'] < 70].head(10)

    st.dataframe(
        problematic_data[['provider', 'contract_number', 'plan_name', 'data_quality_score', 'issues', 'processing_time_hours']],
        use_container_width=True
    )

elif st.session_state.demo_stage == 'pre_ingestion':
    st.markdown("""
    <div class="solution-card">
        <h2>🤖 AI-Powered Pre-Ingestion Intelligence</h2>
        <p>Transform 400+ chaotic templates into clean, standardized data</p>
    </div>
    """, unsafe_allow_html=True)

    # File upload simulation
    st.subheader("📤 Live PAL File Processing Demo")

    col1, col2 = st.columns([1, 2])

    with col1:
        # Simulate file upload
        uploaded_files = st.file_uploader(
            "Drop your PAL files here",
            accept_multiple_files=True,
            type=['csv', 'xlsx', 'xml', 'txt'],
            help="Upload sample PAL files to see AI processing in action"
        )

        if not uploaded_files:
            st.info("👆 Upload files or click 'Demo Mode' to see AI in action")

        demo_mode = st.button("🚀 Demo Mode: Process Sample Files", type="primary")

        if demo_mode or uploaded_files:
            # Simulate AI processing
            with st.spinner("🤖 AI Processing Pipeline Running..."):
                progress_bar = st.progress(0)
                status_text = st.empty()

                steps = [
                    "📄 Detecting file format...",
                    "🔍 Analyzing template structure...",
                    "🧠 AI template matching (400+ templates)...",
                    "✨ Smart field mapping...",
                    "🔧 Data standardization...",
                    "✅ Quality validation...",
                    "📊 Generating insights..."
                ]

                for i, step in enumerate(steps):
                    status_text.text(step)
                    progress_bar.progress((i + 1) / len(steps))
                    time.sleep(0.8)

                st.success("✅ AI Processing Complete!")

    with col2:
        if demo_mode or uploaded_files or st.session_state.get('ai_processed'):
            st.session_state.ai_processed = True

            # AI Processing Results
            st.subheader("🎯 AI Processing Results")

            # Metrics
            col_a, col_b, col_c, col_d = st.columns(4)

            with col_a:
                st.metric("Template Match", "98.5%", "↑12%")
            with col_b:
                st.metric("Processing Time", "12 min", "↓85%")
            with col_c:
                st.metric("Data Quality", "94.2%", "↑28%")
            with col_d:
                st.metric("Auto-Resolved", "156/187", "↑91%")

            # Template detection results
            st.subheader("🔍 Smart Template Detection")

            template_results = pd.DataFrame({
                'File': ['Fidelity_Q3_2024.csv', 'Vanguard_Sept.xlsx', 'TRP_Quarterly.xml'],
                'Detected Template': ['Fidelity Standard v2.1', 'Vanguard Institutional v3.4', 'T.Rowe Price XML v1.8'],
                'Confidence': [99.2, 97.8, 94.1],
                'Issues Found': [2, 5, 12],
                'Auto-Fixed': [2, 4, 10]
            })

            # Color code by confidence
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

            # Field mapping visualization
            st.subheader("🗺️ AI Field Mapping")

            mapping_data = {
                'PAL Field': ['CONT_NUM', 'PLN_NM', 'AST_VAL', 'PARTIC_CNT', 'DT_ASOF'],
                'Standard Field': ['Contract_Number', 'Plan_Name', 'Asset_Value', 'Participant_Count', 'As_Of_Date'],
                'Confidence': [99.8, 94.2, 99.9, 98.1, 87.3],
                'Transformation': ['Direct Map', 'Text Clean', 'Currency Parse', 'Number Parse', 'Date Standard']
            }

            mapping_df = pd.DataFrame(mapping_data)

            fig_mapping = px.bar(
                mapping_df,
                x='PAL Field',
                y='Confidence',
                color='Confidence',
                title="AI Field Mapping Confidence Scores",
                color_continuous_scale=['#FF7043', '#4DD0E1', '#26C6DA']
            )
            fig_mapping.update_layout(yaxis_title="Confidence %")
            st.plotly_chart(fig_mapping, use_container_width=True)

elif st.session_state.demo_stage == 'post_ingestion':
    st.markdown("""
    <div class="solution-card">
        <h2>⚡ Process Automation: Post-Ingestion</h2>
        <p>Intelligent workflows that minimize manual intervention</p>
    </div>
    """, unsafe_allow_html=True)

    # Plan matching demo
    st.subheader("🎯 AI-Powered Plan Matching")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📋 Incoming PAL Plans")

        incoming_plans = pd.DataFrame({
            'Contract_Number': ['CNT-45289', '', 'CNT-78934', 'CNT-12456'],
            'Plan_Name': ['ABC Corp 401K Plan', 'XYZ Company Retirement', 'DEF Inc 401(k) Plan', 'GHI Corp Plan'],
            'Client_Name': ['ABC Corporation', 'XYZ Company LLC', 'DEF Industries', 'GHI Corp'],
            'Assets': ['$2.5M', '$890K', '$5.2M', '$1.8M']
        })

        st.dataframe(incoming_plans, use_container_width=True)

        if st.button("🚀 Run AI Matching", type="primary"):
            with st.spinner("🤖 AI analyzing plan relationships..."):
                time.sleep(2)
                st.success("✅ Matching complete!")

    with col2:
        st.markdown("#### 🎯 AI Matching Results")

        if st.session_state.get('matching_complete'):
            matching_results = pd.DataFrame({
                'PAL Plan': ['ABC Corp 401K Plan', 'XYZ Company Retirement', 'DEF Inc 401(k) Plan', 'GHI Corp Plan'],
                'Matched Plan': ['ABC Corp 401(k)', 'XYZ Co. Retirement Plan', 'DEF Industries 401(k)', 'New Plan'],
                'Confidence': [94.8, 87.2, 99.1, 0.0],
                'Action': ['Auto-Sync', 'Review Required', 'Auto-Sync', 'Manual Setup']
            })

            # Color code by confidence
            def color_matching(row):
                if row['Confidence'] > 90:
                    return ['background-color: #d4edda'] * len(row)
                elif row['Confidence'] > 80:
                    return ['background-color: #fff3cd'] * len(row)
                else:
                    return ['background-color: #f8d7da'] * len(row)

            st.dataframe(
                matching_results.style.apply(color_matching, axis=1),
                use_container_width=True
            )
        else:
            st.info("👆 Run AI matching to see results")

    # Fund Association Intelligence
    st.subheader("💰 Smart Fund Association")

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

        # High confidence matches
        high_confidence = fund_data[fund_data['match_confidence'] > 0.9]
        st.metric("Auto-Matched Funds", f"{len(high_confidence)}/{len(fund_data)}", f"{len(high_confidence)/len(fund_data)*100:.1f}%")

    with col2:
        # Show funds requiring review
        st.markdown("#### 🔍 Funds Requiring Review")

        review_funds = fund_data[fund_data['requires_review']].head(8)

        st.dataframe(
            review_funds[['pal_fund_name', 'master_fund_name', 'match_confidence', 'ticker']],
            use_container_width=True
        )

        st.info(f"💡 AI reduced manual review from {len(fund_data)} to {len(review_funds)} funds ({len(review_funds)/len(fund_data)*100:.0f}% reduction)")

    # Exception handling with AI insights
    st.subheader("🚨 Intelligent Exception Handling")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>🔍 Anomaly Detection</h4>
            <p>AI identified 3 unusual asset movements requiring attention</p>
            <ul>
                <li>Plan ABC: 45% asset increase</li>
                <li>Plan XYZ: New fund addition</li>
                <li>Plan DEF: Missing quarterly data</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>🎯 Predictive Insights</h4>
            <p>Based on historical patterns:</p>
            <ul>
                <li>Plan GHI: Likely fee structure change</li>
                <li>Plan JKL: Probable fund lineup update</li>
                <li>Plan MNO: Expected participant growth</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>⚡ Auto-Resolution</h4>
            <p>AI automatically handled:</p>
            <ul>
                <li>12 minor data formatting issues</li>
                <li>8 fund name standardizations</li>
                <li>5 contract number corrections</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

else:  # future stage
    st.markdown("""
    <div class="solution-card">
        <h2>🌟 Building Your Data Backbone</h2>
        <p>The Future of PAL Processing at RPAG</p>
    </div>
    """, unsafe_allow_html=True)

    # ROI Comparison
    st.subheader("📊 The Transformation: Before vs After AI")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📈 Current State (Manual Process)")

        current_metrics = {
            'Processing Time': '6.5 hours avg',
            'Data Quality Score': '68%',
            'Manual Review Required': '89%',
            'Exception Resolution': '2.3 hours avg',
            'Quarterly Processing': '2-3 business days'
        }

        for metric, value in current_metrics.items():
            st.markdown(f"**{metric}:** {value}")

    with col2:
        st.markdown("#### 🚀 AI-Powered Future")

        future_metrics = {
            'Processing Time': '15 minutes avg ⚡',
            'Data Quality Score': '94% ✨',
            'Manual Review Required': '12% 🎯',
            'Exception Resolution': '5 minutes avg ⚡',
            'Quarterly Processing': '2 hours 🚀'
        }

        for metric, value in future_metrics.items():
            st.markdown(f"**{metric}:** {value}")

    # Visual impact
    st.subheader("🎯 Impact Visualization")

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

    # Future roadmap
    st.subheader("🗺️ AI Implementation Roadmap")

    roadmap_data = {
        'Phase': ['Phase 1: Template Intelligence', 'Phase 2: Smart Matching', 'Phase 3: Predictive Analytics', 'Phase 4: Full Automation'],
        'Timeline': ['Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025'],
        'Key Features': [
            'Auto template detection, Field mapping, Data validation',
            'AI plan matching, Fund associations, Exception handling',
            'Anomaly detection, Trend analysis, Risk prediction',
            'End-to-end automation, Self-optimizing, Continuous learning'
        ],
        'Expected Impact': ['60% time reduction', '80% time reduction', '90% time reduction', '95% time reduction']
    }

    roadmap_df = pd.DataFrame(roadmap_data)
    st.dataframe(roadmap_df, use_container_width=True)

    # Call to action
    st.markdown("""
    <div class="solution-card">
        <h3>🚀 The Power to GROW</h3>
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
    st.subheader("📈 Summary: Empowering the Automation Advocates")

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

with col1:
    if st.button("⏮️ Previous", disabled=(selected_stage == 'intro')):
        stages_list = list(demo_stages.keys())
        current_idx = stages_list.index(selected_stage)
        if current_idx > 0:
            st.session_state.demo_stage = stages_list[current_idx - 1]
            st.experimental_rerun()

with col2:
    st.markdown(f"<center><strong>{demo_stages[selected_stage]}</strong></center>", unsafe_allow_html=True)

with col3:
    if st.button("Next ⏭️", disabled=(selected_stage == 'future')):
        stages_list = list(demo_stages.keys())
        current_idx = stages_list.index(selected_stage)
        if current_idx < len(stages_list) - 1:
            st.session_state.demo_stage = stages_list[current_idx + 1]
            st.experimental_rerun()