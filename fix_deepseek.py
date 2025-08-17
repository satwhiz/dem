# =============================================================================
# File: clean_deepseek_config.py - Proper DeepSeek Configuration
# =============================================================================

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

class DeepSeekConfig:
    """Clean DeepSeek configuration with proper naming conventions"""
    
    @staticmethod
    def setup_environment():
        """Setup DeepSeek environment with clear naming"""
        load_dotenv()
        
        # Use clear DeepSeek-specific environment variables
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        deepseek_model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        deepseek_base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        
        if not deepseek_key:
            raise ValueError("""
            DeepSeek API key not found! 
            Please set DEEPSEEK_API_KEY in your .env file:
            DEEPSEEK_API_KEY=your_deepseek_key_here
            """)
        
        # For LiteLLM compatibility, we need the deepseek/ prefix
        if not deepseek_model.startswith("deepseek/"):
            litellm_model = f"deepseek/{deepseek_model}"
        else:
            litellm_model = deepseek_model
        
        config = {
            "api_key": deepseek_key,
            "base_url": deepseek_base_url,
            "model": deepseek_model,  # Clean model name
            "litellm_model": litellm_model,  # Model name for LiteLLM
            "temperature": float(os.getenv("DEEPSEEK_TEMPERATURE", "0.7")),
            "max_tokens": int(os.getenv("DEEPSEEK_MAX_TOKENS", "4000"))
        }
        
        return config
    
    @staticmethod
    def create_llm():
        """Create a properly configured LangChain LLM for DeepSeek"""
        config = DeepSeekConfig.setup_environment()
        
        # Create LangChain LLM with DeepSeek configuration
        llm = ChatOpenAI(
            model=config["litellm_model"],  # Use LiteLLM format for compatibility
            openai_api_key=config["api_key"],  # DeepSeek key (confusing but necessary)
            openai_api_base=config["base_url"],  # DeepSeek base URL
            temperature=config["temperature"],
            max_tokens=config["max_tokens"],
            model_kwargs={
                "extra_headers": {
                    "User-Agent": "TrialBalance-CrewAI/1.0"
                }
            }
        )
        
        return llm
    
    @staticmethod
    def create_crewai_agent(role, goal, backstory, tools=None, **kwargs):
        """Create a CrewAI agent with DeepSeek LLM"""
        from crewai import Agent
        
        llm = DeepSeekConfig.create_llm()
        
        agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools or [],
            llm=llm,  # Pass the configured LLM
            verbose=kwargs.get('verbose', True),
            allow_delegation=kwargs.get('allow_delegation', False),
            **kwargs
        )
        
        return agent
    
    @staticmethod
    def print_config():
        """Print configuration for debugging"""
        try:
            config = DeepSeekConfig.setup_environment()
            print("🔍 DeepSeek Configuration:")
            print(f"   Provider: DeepSeek AI")
            print(f"   Model: {config['model']}")
            print(f"   LiteLLM Model: {config['litellm_model']}")
            print(f"   Base URL: {config['base_url']}")
            print(f"   API Key: {config['api_key'][:8]}..." if config['api_key'] else "Not set")
            print(f"   Temperature: {config['temperature']}")
            print(f"   Max Tokens: {config['max_tokens']}")
            
            print("\n📝 Why this naming?")
            print("   - DEEPSEEK_API_KEY: Your actual DeepSeek key (clear naming)")
            print("   - openai_api_key param: Required by LangChain for compatibility")
            print("   - deepseek/ prefix: Required by LiteLLM to identify provider")
            
        except Exception as e:
            print(f"❌ Configuration error: {e}")

# =============================================================================
# File: .env (CLEAN VERSION)
# =============================================================================

clean_env_template = """# ========================================
# DeepSeek AI Configuration (Clear Naming)
# ========================================

# Your DeepSeek API key from https://platform.deepseek.com/
DEEPSEEK_API_KEY=sk-e941fc978b6144258a388c4c0f6553c4

# DeepSeek API settings
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_TEMPERATURE=0.7
DEEPSEEK_MAX_TOKENS=4000

# Available Models:
# deepseek-chat - General purpose (recommended)
# deepseek-coder - Code-focused
# deepseek-reasoner - Enhanced reasoning

# ========================================
# Why not OPENAI_API_KEY?
# ========================================
# We use DEEPSEEK_API_KEY for clarity, but internally
# LangChain still expects OpenAI-compatible parameters
# for technical compatibility reasons.
"""

# =============================================================================
# File: test_clean_deepseek.py - Test the Clean Configuration
# =============================================================================

def test_clean_config():
    """Test the clean DeepSeek configuration"""
    print("🧪 Testing Clean DeepSeek Configuration")
    print("=" * 45)
    
    try:
        from clean_deepseek_config import DeepSeekConfig
        
        # Test configuration
        print("\n1️⃣ Testing Configuration:")
        DeepSeekConfig.print_config()
        
        # Test LLM creation
        print("\n2️⃣ Testing LLM Creation:")
        llm = DeepSeekConfig.create_llm()
        print("✅ LLM created successfully")
        
        # Test direct LLM call
        print("\n3️⃣ Testing Direct LLM Call:")
        from langchain.schema import HumanMessage
        
        response = llm.invoke([HumanMessage(content="Say hello from DeepSeek!")])
        print(f"✅ LLM Response: {response.content}")
        
        # Test CrewAI agent creation
        print("\n4️⃣ Testing CrewAI Agent:")
        agent = DeepSeekConfig.create_crewai_agent(
            role="Test Agent",
            goal="Test DeepSeek integration",
            backstory="You are testing the clean DeepSeek configuration.",
            verbose=False
        )
        print("✅ CrewAI agent created successfully")
        
        # Test CrewAI workflow
        print("\n5️⃣ Testing Full CrewAI Workflow:")
        from crewai import Task, Crew, Process
        
        task = Task(
            description="Say 'Hello from clean DeepSeek configuration!' and nothing else.",
            agent=agent,
            expected_output="A brief hello message"
        )
        
        crew = Crew(
            agents=[agent],
            tasks=[task], 
            process=Process.sequential,
            verbose=False
        )
        
        result = crew.kickoff()
        print(f"✅ CrewAI Result: {result}")
        
        print("\n🎉 All tests passed! Clean configuration working.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

# =============================================================================
# File: updated_simple_demo.py - Using Clean Configuration
# =============================================================================

def create_clean_demo():
    """Create demo using clean DeepSeek configuration"""
    
    demo_content = '''import os
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
        print("\\n🔍 DeepSeek Configuration:")
        DeepSeekConfig.print_config()
        
        # Create agent using clean configuration
        print("\\n🤖 Creating Financial Analyst Agent...")
        analyst = DeepSeekConfig.create_crewai_agent(
            role='Senior Financial Data Analyst',
            goal='Analyze trial balance data and provide expert insights',
            backstory="""You are a senior financial analyst with 15+ years of experience 
            in trial balance processing, variance analysis, and tax provision preparation. 
            You provide accurate, actionable insights for business decisions.""",
            verbose=True
        )
        
        # Load demo data
        print("\\n📊 Loading Trial Balance Data...")
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
        print("\\n🚀 Running Financial Analysis...")
        crew = Crew(
            agents=[analyst],
            tasks=[analysis_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        # Save results
        print("\\n💾 Saving Results...")
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
        
        print(f"\\n🎉 Analysis Complete!")
        print(f"📁 Results saved to: {output_file}")
        print(f"🤖 Powered by: DeepSeek AI")
        
        return True
        
    except Exception as e:
        print(f"\\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    clean_trial_balance_demo()
'''
    
    with open('clean_demo.py', 'w') as f:
        f.write(demo_content)
    
    print("✅ Created clean_demo.py with proper DeepSeek naming")

# =============================================================================
# Main Setup Function
# =============================================================================

def setup_clean_deepseek():
    """Set up clean DeepSeek configuration"""
    print("🚀 Setting Up Clean DeepSeek Configuration")
    print("=" * 45)
    
    # Create clean .env file
    print("\n1️⃣ Creating clean .env file...")
    with open('.env', 'w') as f:
        f.write(clean_env_template)
    print("✅ Created .env with DEEPSEEK_API_KEY naming")
    
    # Create clean config file
    print("\n2️⃣ Creating clean configuration...")
    # (The clean_deepseek_config.py content is already defined above)
    print("✅ Use the clean_deepseek_config.py from the artifact")
    
    # Create test file
    print("\n3️⃣ Creating test script...")
    # (The test function is already defined above)
    print("✅ Use test_clean_config() function")
    
    # Create demo
    print("\n4️⃣ Creating clean demo...")
    create_clean_demo()
    
    print(f"\n🎉 Clean DeepSeek setup complete!")
    print(f"\n📝 Next steps:")
    print(f"1. Update your API key in .env:")
    print(f"   DEEPSEEK_API_KEY=sk-e941fc978b6144258a388c4c0f6553c4")
    print(f"2. Test: python -c \"from clean_deepseek_config import *; test_clean_config()\"")
    print(f"3. Run demo: python clean_demo.py")

if __name__ == "__main__":
    setup_clean_deepseek()