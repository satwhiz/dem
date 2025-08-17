import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime
import sys

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from dynamic_demo import DynamicTrialBalanceSystem

# Page configuration
st.set_page_config(
    page_title="Trial Balance Automation Demo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.sub-header {
    font-size: 1.5rem;
    color: #2e86ab;
    margin: 1rem 0;
}
.metric-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}
.demo-section {
    border: 2px solid #e1e5e9;
    border-radius: 0.5rem;
    padding: 1.5rem;
    margin: 1rem 0;
}
.success-message {
    background-color: #d4edda;
    color: #155724;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'demo_results' not in st.session_state:
        st.session_state.demo_results = {}
    if 'system' not in st.session_state:
        st.session_state.system = DynamicTrialBalanceSystem()
    if 'demo_data_loaded' not in st.session_state:
        st.session_state.demo_data_loaded = False

def load_demo_data():
    """Load demonstration data"""
    try:
        data_files = {
            'SAP_2024': 'data/test/sap_full_year_2024.csv',
            'Oracle_Q2': 'data/test/oracle_q2_2024.csv',
            'Excel_2023': 'data/test/excel_export_2023.csv'
        }
        
        loaded_data = {}
        for name, file_path in data_files.items():
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                loaded_data[name] = df
            else:
                st.warning(f"Demo data file not found: {file_path}")
        
        return loaded_data
    except Exception as e:
        st.error(f"Error loading demo data: {e}")
        return {}

def show_data_overview(data_dict):
    """Show overview of loaded data"""
    st.markdown('<div class="sub-header">📊 Demo Data Overview</div>', unsafe_allow_html=True)
    
    cols = st.columns(len(data_dict))
    
    for i, (name, df) in enumerate(data_dict.items()):
        with cols[i]:
            st.markdown(f"""
            <div class="metric-card">
                <h4>{name}</h4>
                <p><strong>Records:</strong> {len(df)}</p>
                <p><strong>Columns:</strong> {len(df.columns)}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show sample data
            with st.expander(f"Preview {name}"):
                st.dataframe(df.head(), use_container_width=True)

def create_data_visualization(data_dict):
    """Create visualizations of the demo data"""
    st.markdown('<div class="sub-header">📈 Data Visualizations</div>', unsafe_allow_html=True)
    
    # SAP data analysis
    if 'SAP_2024' in data_dict:
        df_sap = data_dict['SAP_2024']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("SAP Account Balances by Period")
            
            # Prepare data for visualization
            df_sap['period_date'] = pd.to_datetime(df_sap['period_ending'])
            df_sap['net_balance'] = df_sap['dr_amount'] - df_sap['cr_amount']
            df_sap['period_label'] = df_sap['period_date'].dt.strftime('%Y-%m')
            
            # Group by period and account type
            monthly_summary = df_sap.groupby(['period_label', 'gl_account'])['net_balance'].sum().reset_index()
            
            fig = px.bar(
                monthly_summary.head(20), 
                x='period_label', 
                y='net_balance', 
                color='gl_account',
                title='Account Balances by Month',
                labels={'net_balance': 'Net Balance ($)', 'period_label': 'Period'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Account Distribution")
            
            # Account type distribution
            account_ranges = {
                'Assets (1000-1999)': df_sap[df_sap['gl_account'].between(1000, 1999)]['net_balance'].sum(),
                'Liabilities (2000-2999)': abs(df_sap[df_sap['gl_account'].between(2000, 2999)]['net_balance'].sum()),
                'Equity (3000-3999)': abs(df_sap[df_sap['gl_account'].between(3000, 3999)]['net_balance'].sum()),
                'Revenue (4000-4999)': abs(df_sap[df_sap['gl_account'].between(4000, 4999)]['net_balance'].sum()),
                'Expenses (5000-5999)': df_sap[df_sap['gl_account'].between(5000, 5999)]['net_balance'].sum()
            }
            
            fig_pie = px.pie(
                values=list(account_ranges.values()),
                names=list(account_ranges.keys()),
                title='Trial Balance by Account Type'
            )
            st.plotly_chart(fig_pie, use_container_width=True)

def run_ai_analysis_demo():
    """Interactive AI analysis demo"""
    st.markdown('<div class="demo-section">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">🤖 AI-Powered Analysis Demo</div>', unsafe_allow_html=True)
    
    # Pre-defined demo scenarios
    demo_scenarios = {
        "🆕 New Account Detection": {
            "request": "Analyze Q1 2024 for new accounts and categorize them",
            "files": ["data/test/sap_full_year_2024.csv"],
            "labels": ["SAP_Data"],
            "description": "Identifies new accounts that appeared in Q1 2024 and provides proper categorization"
        },
        "📊 Variance Analysis": {
            "request": "Compare Q1 vs Q2 2024 for material variances",
            "files": ["data/test/sap_full_year_2024.csv"],
            "labels": ["SAP_Data"],
            "description": "Analyzes period-over-period changes and flags significant variances"
        },
        "🔄 Multi-System Comparison": {
            "request": "Compare SAP vs Oracle trial balance data",
            "files": ["data/test/sap_full_year_2024.csv", "data/test/oracle_q2_2024.csv"],
            "labels": ["SAP_System", "Oracle_System"],
            "description": "Reconciles trial balances from different ERP systems with automatic schema mapping"
        },
        "📋 Tax Provision Analysis": {
            "request": "Categorize accounts for tax provision and identify deductible expenses",
            "files": ["data/test/oracle_q2_2024.csv"],
            "labels": ["Q2_Data"],
            "description": "Provides tax categorization and identifies potential tax savings opportunities"
        }
    }
    
    # Scenario selection
    selected_scenario = st.selectbox(
        "Choose Analysis Scenario:",
        options=list(demo_scenarios.keys()),
        index=0
    )
    
    scenario = demo_scenarios[selected_scenario]
    
    st.info(f"**Scenario:** {scenario['description']}")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Show the request
        st.text_area(
            "AI Analysis Request:",
            value=scenario['request'],
            height=100,
            disabled=True
        )
    
    with col2:
        st.write("**Data Sources:**")
        for i, file in enumerate(scenario['files']):
            st.write(f"• {scenario['labels'][i]}")
    
    # Run analysis button
    if st.button(f"🚀 Run {selected_scenario}", type="primary"):
        with st.spinner("Running AI analysis... This may take 30-60 seconds."):
            try:
                # Run the actual AI analysis
                result = st.session_state.system.run_analysis(
                    scenario['request'],
                    scenario['files'],
                    scenario['labels']
                )
                
                if result:
                    st.markdown('<div class="success-message">✅ Analysis completed successfully!</div>', unsafe_allow_html=True)
                    
                    # Display results
                    st.subheader("🎯 AI Analysis Results")
                    st.write(result)
                    
                    # Store in session state
                    st.session_state.demo_results[selected_scenario] = {
                        'result': result,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                else:
                    st.error("Analysis failed. Please check the logs.")
                    
            except Exception as e:
                st.error(f"Error running analysis: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_analysis_history():
    """Show history of completed analyses"""
    if st.session_state.demo_results:
        st.markdown('<div class="sub-header">📚 Analysis History</div>', unsafe_allow_html=True)
        
        for scenario, data in st.session_state.demo_results.items():
            with st.expander(f"{scenario} - {data['timestamp']}"):
                st.write(data['result'])

def show_system_capabilities():
    """Show system capabilities and architecture"""
    st.markdown('<div class="sub-header">🏗️ System Capabilities</div>', unsafe_allow_html=True)
    
    capabilities = {
        "🤖 Multi-Agent AI": "Specialized agents for different analysis types (Variance, New Accounts, Tax, Compliance)",
        "📊 Schema Auto-Detection": "Automatically handles SAP, Oracle, NetSuite, Excel formats",
        "📅 Period Intelligence": "Smart filtering for Q1, Q2, monthly, yearly analysis",
        "🗣️ Natural Language": "Plain English requests like 'Find new accounts in Q1 2024'",
        "💼 Business Intelligence": "Professional-grade insights with actionable recommendations",
        "🔍 Audit Ready": "Complete audit trails with decision reasoning",
        "⚡ High Performance": "Processes thousands of accounts in minutes",
        "🔧 Integration Ready": "API endpoints for ERP and tax system integration"
    }
    
    cols = st.columns(2)
    
    for i, (feature, description) in enumerate(capabilities.items()):
        col = cols[i % 2]
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <h4>{feature}</h4>
                <p>{description}</p>
            </div>
            """, unsafe_allow_html=True)

def custom_analysis_section():
    """Allow users to run custom analysis"""
    st.markdown('<div class="sub-header">✨ Custom Analysis</div>', unsafe_allow_html=True)
    
    with st.form("custom_analysis"):
        custom_request = st.text_area(
            "Enter your custom analysis request:",
            placeholder="e.g., 'Identify accounts with unusual activity in March 2024'",
            height=100
        )
        
        # File selection
        available_files = [
            "data/test/sap_full_year_2024.csv",
            "data/test/oracle_q2_2024.csv", 
            "data/test/excel_export_2023.csv"
        ]
        
        selected_files = st.multiselect(
            "Select data files:",
            options=available_files,
            default=[available_files[0]]
        )
        
        submitted = st.form_submit_button("Run Custom Analysis")
        
        if submitted and custom_request and selected_files:
            with st.spinner("Running custom analysis..."):
                try:
                    labels = [f"Dataset_{i+1}" for i in range(len(selected_files))]
                    result = st.session_state.system.run_analysis(
                        custom_request,
                        selected_files,
                        labels
                    )
                    
                    if result:
                        st.success("Custom analysis completed!")
                        st.write(result)
                    else:
                        st.error("Analysis failed.")
                        
                except Exception as e:
                    st.error(f"Error: {e}")

def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">🤖 Trial Balance Automation Demo</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">AI-Powered Financial Analysis with Multi-Agent Intelligence</p>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🎯 Demo Navigation")
    
    demo_sections = [
        "📊 Data Overview",
        "🤖 AI Analysis Demo", 
        "✨ Custom Analysis",
        "🏗️ System Capabilities",
        "📚 Analysis History"
    ]
    
    selected_section = st.sidebar.selectbox(
        "Choose Demo Section:",
        demo_sections,
        index=1  # Default to AI Analysis Demo
    )
    
    # Load demo data
    if not st.session_state.demo_data_loaded:
        with st.spinner("Loading demo data..."):
            demo_data = load_demo_data()
            st.session_state.demo_data = demo_data
            st.session_state.demo_data_loaded = True
    
    # Show selected section
    if selected_section == "📊 Data Overview":
        show_data_overview(st.session_state.demo_data)
        create_data_visualization(st.session_state.demo_data)
        
    elif selected_section == "🤖 AI Analysis Demo":
        run_ai_analysis_demo()
        
    elif selected_section == "✨ Custom Analysis":
        custom_analysis_section()
        
    elif selected_section == "🏗️ System Capabilities":
        show_system_capabilities()
        
    elif selected_section == "📚 Analysis History":
        show_analysis_history()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🚀 Powered by DeepSeek AI • Built with CrewAI Multi-Agent Framework</p>
        <p>⚡ Enterprise-Ready Trial Balance Automation</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()