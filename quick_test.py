import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

def quick_user_request_test():
    """Test: Analyze Q1 2024 for new accounts"""
    print("🧪 User Request Test: Q1 2024 New Accounts")
    print("=" * 45)
    
    try:
        # Use the same DeepSeek config that works
        from deepseek_config import DeepSeekConfig
        config = DeepSeekConfig.setup_environment()
        print(f"✅ DeepSeek: {config['model']}")
        
        # Load and filter SAP data to Q1 2024
        print("\n📂 Processing SAP data...")
        df = pd.read_csv('data/test/sap_full_year_2024.csv')
        df['period_date'] = pd.to_datetime(df['period_ending'])
        q1_data = df[(df['period_date'] >= '2024-01-01') & (df['period_date'] <= '2024-03-31')]
        
        print(f"   📊 Q1 2024: {len(q1_data)} records")
        print(f"   🔢 Unique accounts: {q1_data['gl_account'].nunique()}")
        
        # Find accounts that appear later in Q1 (new accounts)
        jan_accounts = set(q1_data[q1_data['period_date'] <= '2024-01-31']['gl_account'])
        mar_accounts = set(q1_data[q1_data['period_date'] >= '2024-03-01']['gl_account'])
        new_accounts = mar_accounts - jan_accounts
        
        print(f"\n🆕 New accounts in Q1:")
        for acc in sorted(new_accounts):
            name = q1_data[q1_data['gl_account'] == acc]['gl_description'].iloc[0]
            print(f"   {acc}: {name}")
        
        # Run AI analysis using working configuration
        from crewai import Agent, Task, Crew, Process
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(
            model=config["model"],
            openai_api_base=config["base_url"],
            openai_api_key=config["api_key"],
            temperature=0.7,
            max_tokens=1000
        )
        
        analyst = Agent(
            role='Account Change Specialist',
            goal='Analyze Q1 2024 for new accounts and categorize them',
            backstory='Expert in chart of accounts analysis and new account detection.',
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
        
        task = Task(
            description=f"""
            Analyze Q1 2024 SAP data for new accounts:
            
            Data Summary:
            - Q1 records: {len(q1_data)}
            - Unique accounts: {q1_data['gl_account'].nunique()}
            - New accounts detected: {list(new_accounts)}
            - Q1 total debits: ${q1_data['dr_amount'].sum():,.2f}
            - Q1 total credits: ${q1_data['cr_amount'].sum():,.2f}
            
            Tasks:
            1. Analyze the new accounts that appeared in Q1
            2. Categorize each new account (Asset, Liability, Revenue, Expense)
            3. Explain the business purpose of each new account
            4. Assess materiality and impact on financial statements
            5. Provide recommendations for proper classification
            
            Focus on practical insights for the finance team.
            """,
            agent=analyst,
            expected_output="Detailed analysis of Q1 2024 new accounts with categorizations and business insights"
        )
        
        crew = Crew(
            agents=[analyst],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        print("\n🤖 Running Q1 New Account Analysis...")
        result = crew.kickoff()
        
        print(f"\n🎉 Analysis completed!")
        
        # Save results
        os.makedirs('data/output', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        import json
        with open(f'data/output/q1_new_accounts_{timestamp}.json', 'w') as f:
            json.dump({
                "request": "Analyze Q1 2024 for new accounts",
                "result": str(result),
                "new_accounts_detected": list(new_accounts),
                "q1_summary": {
                    "total_records": len(q1_data),
                    "unique_accounts": q1_data['gl_account'].nunique(),
                    "total_debits": float(q1_data['dr_amount'].sum()),
                    "total_credits": float(q1_data['cr_amount'].sum())
                }
            }, f, indent=2)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    quick_user_request_test()