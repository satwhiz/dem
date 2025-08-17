# =============================================================================
# File: src/agents/trial_balance_agents.py (UPDATED VERSION)
# =============================================================================

from crewai import Agent
from src.tools.crew_tools import (
    load_trial_balance, 
    categorize_account, 
    variance_analysis,
    validate_compliance,
    prepare_upload_format
)

class TrialBalanceAgents:
    
    def __init__(self):
        # Tools are now imported as functions
        pass
    
    def data_extractor_agent(self):
        return Agent(
            role='Data Extraction Specialist',
            goal='Extract and validate trial balance data from various ERP systems',
            backstory="""You are an expert in financial data extraction with 10+ years 
            of experience working with various ERP systems like SAP, Oracle, and NetSuite. 
            You ensure data quality and completeness before any processing begins.""",
            tools=[load_trial_balance],
            verbose=True,
            allow_delegation=False,
            max_iter=2
        )
    
    def categorization_agent(self):
        return Agent(
            role='Account Categorization Expert',
            goal='Accurately categorize all accounts for tax reporting purposes',
            backstory="""You are a senior tax accountant with deep knowledge of 
            chart of accounts structures and tax categorization rules. You ensure 
            every account is properly classified for accurate tax provision calculations.""",
            tools=[categorize_account],
            verbose=True,
            allow_delegation=False,
            max_iter=3
        )
    
    def new_account_identifier_agent(self):
        return Agent(
            role='New Account Detection Specialist',
            goal='Identify and properly categorize new accounts that appear in current period',
            backstory="""You are a financial analyst specialized in detecting changes 
            in chart of accounts. You have a keen eye for spotting new accounts and 
            understanding their business purpose for proper categorization.""",
            tools=[variance_analysis, categorize_account],
            verbose=True,
            allow_delegation=True,
            max_iter=2
        )
    
    def variance_analyzer_agent(self):
        return Agent(
            role='Financial Variance Analyst',
            goal='Analyze period-over-period variances and identify material changes',
            backstory="""You are a financial analyst with expertise in variance analysis. 
            You identify unusual fluctuations in account balances and provide insights 
            into potential causes, helping ensure accuracy in financial reporting.""",
            tools=[variance_analysis],
            verbose=True,
            allow_delegation=False,
            max_iter=2
        )
    
    def compliance_reviewer_agent(self):
        return Agent(
            role='Compliance and Quality Assurance Specialist',
            goal='Ensure trial balance meets all compliance requirements and quality standards',
            backstory="""You are a compliance officer with extensive experience in 
            financial controls and audit requirements. You perform final quality checks 
            to ensure data integrity and regulatory compliance.""",
            tools=[validate_compliance],
            verbose=True,
            allow_delegation=False,
            max_iter=2
        )
    
    def uploader_agent(self):
        return Agent(
            role='Tax Provision System Integration Specialist',
            goal='Format and upload processed data to tax provision systems',
            backstory="""You are a tax technology specialist who ensures seamless 
            integration with tax provision software like OneSource and Corptax. 
            You handle data formatting and upload validation.""",
            tools=[prepare_upload_format],
            verbose=True,
            allow_delegation=False,
            max_iter=1
        )