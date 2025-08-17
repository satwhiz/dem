# =============================================================================
# File: simple_demo.py (Create this as a temporary fix)
# =============================================================================

import os
import sys
import pandas as pd
import json
from datetime import datetime
from dotenv import load_dotenv

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking prerequisites...")
    
    # Check data files
    required_files = [
        'data/input/trial_balance_2024.csv',
        'data/reference/trial_balance_2023.csv',
        'src/config/account_mapping.json'
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ Missing required file: {file_path}")
            return False
        print(f"✅ Found: {file_path}")
    
    # Check environment
    load_dotenv()
    
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OpenAI API key not found in environment")
        return False
    print("✅ OpenAI API key configured")
    
    return True

def simple_crew_demo():
    """Run a simplified CrewAI demo with basic agents"""
    print("\n🚀 Starting Simplified CrewAI Demo...")
    print("=" * 50)
    
    try:
        from crewai import Agent, Task, Crew, Process
        
        # Create a simple agent without custom tools
        data_analyst = Agent(
            role='Senior Financial Data Analyst',
            goal='Analyze trial balance data and provide insights',
            backstory="""You are a senior financial analyst with 15+ years of experience 
            in trial balance processing, variance analysis, and tax provision preparation. 
            You have expertise in identifying new accounts, material variances, and ensuring data quality.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Load actual data for context
        df_2024 = pd.read_csv('data/input/trial_balance_2024.csv')
        df_2023 = pd.read_csv('data/reference/trial_balance_2023.csv')
        
        # Calculate some basic stats
        total_debits_2024 = df_2024['debit'].sum()
        total_credits_2024 = df_2024['credit'].sum()
        accounts_2024 = len(df_2024)
        accounts_2023 = len(df_2023)
        new_accounts = accounts_2024 - accounts_2023
        
        # Create a comprehensive task
        analysis_task = Task(
            description=f"""
            Analyze the Q4 2024 trial balance data and provide a comprehensive report.
            
            Current Period Data Summary:
            - Total accounts: {accounts_2024}
            - Total debits: ${total_debits_2024:,.2f}
            - Total credits: ${total_credits_2024:,.2f}
            - New accounts since 2023: {new_accounts}
            
            Key accounts for analysis:
            1. Account 1150: Prepaid Expenses (NEW) - $15,000 debit
            2. Account 2200: Customer Deposits (NEW) - $20,000 credit  
            3. Account 5300: Marketing Expenses (NEW) - $25,000 debit
            4. Account 5400: Technology Expenses (NEW) - $18,000 debit
            5. Account 1100: Accounts Receivable - increased from $85,000 to $125,000 (+47%)
            6. Account 5100: Operating Expenses - increased from $80,000 to $120,000 (+50%)
            
            Your tasks:
            1. Analyze the 4 new accounts and categorize them appropriately
            2. Evaluate the material variances in Accounts Receivable and Operating Expenses
            3. Assess overall trial balance quality and compliance
            4. Provide recommendations for the tax provision process
            5. Flag any items requiring management attention
            
            Provide a detailed analysis report with:
            - New account categorizations with reasoning
            - Variance analysis with potential explanations  
            - Data quality assessment
            - Tax provision implications
            - Risk areas and recommendations
            """,
            agent=data_analyst,
            expected_output="A comprehensive trial balance analysis report with categorizations, variance explanations, compliance assessment, and actionable recommendations"
        )
        
        # Create and run crew
        crew = Crew(
            agents=[data_analyst],
            tasks=[analysis_task],
            process=Process.sequential,
            verbose=True
        )
        
        print("\n📊 Running Trial Balance Analysis...")
        print("-" * 40)
        
        result = crew.kickoff()
        
        # Save results
        os.makedirs('data/output', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        output_data = {
            "demo_type": "Simplified CrewAI Trial Balance Demo",
            "timestamp": timestamp,
            "analysis_result": str(result),
            "data_summary": {
                "total_accounts_2024": accounts_2024,
                "total_accounts_2023": accounts_2023,
                "new_accounts_detected": new_accounts,
                "total_debits": float(total_debits_2024),
                "total_credits": float(total_credits_2024),
                "balance_difference": float(total_debits_2024 - total_credits_2024)
            }
        }
        
        output_file = f"data/output/simple_demo_results_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\n🎉 Demo completed successfully!")
        print(f"📁 Results saved to: {output_file}")
        print(f"📊 Analyzed {accounts_2024} accounts")
        print(f"🆕 Detected {new_accounts} new accounts")
        print(f"💰 Total debits: ${total_debits_2024:,.2f}")
        print(f"✅ Analysis complete!")
        
        return result
        
    except Exception as e:
        print(f"❌ Error in crew demo: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main entry point for the simplified demo"""
    print("🎬 Simplified Trial Balance Automation Demo")
    print("=" * 50)
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please check setup.")
        return 1
    
    # Run the demo
    result = simple_crew_demo()
    
    if result:
        print(f"\n🕒 Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return 0
    else:
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)