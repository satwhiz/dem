import os
import sys
import pandas as pd
import json
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from clean_deepseek_config import DeepSeekConfig
from crewai import Task, Crew, Process

def clean_trial_balance_demo():
    """Trial balance demo with clean DeepSeek configuration"""
    print("🎬 Trial Balance Demo (Clean DeepSeek Config)")
    print("=" * 50)
    
    try:
        # Show configuration
        print("\n🔍 DeepSeek Configuration:")
        DeepSeekConfig.print_config()
        
        # Create agent using clean configuration
        print("\n🤖 Creating Financial Analyst Agent...")
        analyst = DeepSeekConfig.create_crewai_agent(
            role='Senior Financial Data Analyst',
            goal='Analyze trial balance data and provide expert insights',
            backstory="""You are a senior financial analyst with 15+ years of experience 
            in trial balance processing, variance analysis, and tax provision preparation. 
            You provide accurate, actionable insights for business decisions.""",
            verbose=True
        )
        
        # Load demo data
        print("\n📊 Loading Trial Balance Data...")
        try:
            df_2024 = pd.read_csv('data/input/trial_balance_2024.csv')
            df_2023 = pd.read_csv('data/reference/trial_balance_2023.csv')
            
            accounts_2024 = len(df_2024)
            accounts_2023 = len(df_2023)
            total_debits = df_2024['debit'].sum()
            total_credits = df_2024['credit'].sum()
            new_accounts = accounts_2024 - accounts_2023
            
            print(f"   ✅ 2024 Data: {accounts_2024} accounts")
            print(f"   ✅ 2023 Data: {accounts_2023} accounts") 
            print(f"   ✅ New Accounts: {new_accounts}")
            
        except FileNotFoundError:
            print("   ⚠️  Demo data files not found, using sample data...")
            accounts_2024 = 14
            accounts_2023 = 10
            total_debits = 828000
            total_credits = 800000
            new_accounts = 4
        
        # Create analysis task
        analysis_task = Task(
            description=f"""
            Analyze Q4 2024 trial balance data and provide insights:
            
            Data Summary:
            - Total accounts 2024: {accounts_2024}
            - Total accounts 2023: {accounts_2023}
            - New accounts: {new_accounts}
            - Total debits: ${total_debits:,.2f}
            - Total credits: ${total_credits:,.2f}
            
            Key Analysis Points:
            1. Identify the {new_accounts} new accounts and categorize them
            2. Analyze material variances (Accounts Receivable +47%, Operating Expenses +50%)
            3. Assess trial balance quality (${total_debits - total_credits:,.2f} imbalance)
            4. Provide tax provision recommendations
            5. Flag areas requiring management attention
            
            Provide a comprehensive financial analysis with specific insights and recommendations.
            """,
            agent=analyst,
            expected_output="A detailed financial analysis with categorizations, variance explanations, and actionable business recommendations"
        )
        
        # Execute analysis
        print("\n🚀 Running Financial Analysis...")
        crew = Crew(
            agents=[analyst],
            tasks=[analysis_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        # Save results
        print("\n💾 Saving Results...")
        os.makedirs('data/output', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        output_data = {
            "demo_type": "Clean DeepSeek Trial Balance Analysis",
            "timestamp": timestamp,
            "provider": "DeepSeek AI",
            "model_used": "deepseek-chat",
            "analysis_result": str(result),
            "data_summary": {
                "accounts_2024": accounts_2024,
                "accounts_2023": accounts_2023,
                "new_accounts": new_accounts,
                "total_debits": float(total_debits),
                "total_credits": float(total_credits)
            }
        }
        
        output_file = f"data/output/clean_deepseek_demo_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\n🎉 Analysis Complete!")
        print(f"📁 Results saved to: {output_file}")
        print(f"🤖 Powered by: DeepSeek AI")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    clean_trial_balance_demo()
