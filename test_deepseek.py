import os
from dotenv import load_dotenv
from deepseek_config import DeepSeekConfig

def test_deepseek_connection():
    """Test DeepSeek API connection with proper configuration"""
    print("🧪 Testing DeepSeek API Connection (Fixed)")
    print("=" * 45)
    
    try:
        # Setup configuration
        config = DeepSeekConfig.setup_environment()
        print(f"✅ Configuration loaded:")
        print(f"   Model: {config['model']}")
        print(f"   Base URL: {config['base_url']}")
        print(f"   API Key: {config['api_key'][:8]}..." if config['api_key'] else "   API Key: Not set")
        
        # Test with a simple CrewAI agent using proper LLM configuration
        from crewai import Agent, Task, Crew, Process
        from langchain_openai import ChatOpenAI
        
        # Create LLM instance with proper configuration
        llm = ChatOpenAI(
            model=config["model"],
            openai_api_base=config["base_url"],
            openai_api_key=config["api_key"],
            temperature=config["temperature"],
            max_tokens=config["max_tokens"]
        )
        
        test_agent = Agent(
            role='Test Agent',
            goal='Test DeepSeek API connection',
            backstory='You are a test agent to verify API connectivity.',
            verbose=True,
            allow_delegation=False,
            llm=llm  # Pass the LLM instance directly
        )
        
        test_task = Task(
            description="Say hello and confirm you are working with DeepSeek API. Keep it brief - just say 'Hello from DeepSeek!'",
            agent=test_agent,
            expected_output="A brief hello message confirming DeepSeek connectivity"
        )
        
        test_crew = Crew(
            agents=[test_agent],
            tasks=[test_task],
            process=Process.sequential,
            verbose=True
        )
        
        print("\n🚀 Testing API call...")
        result = test_crew.kickoff()
        
        print(f"\n✅ DeepSeek API Test Successful!")
        print(f"Response: {result}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ DeepSeek API Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_only():
    """Test configuration without API call"""
    print("🔍 Testing DeepSeek Configuration")
    print("=" * 35)
    
    try:
        DeepSeekConfig.print_config()
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_direct_llm():
    """Test direct LLM call without CrewAI"""
    print("🧪 Testing Direct DeepSeek LLM Call")
    print("=" * 35)
    
    try:
        config = DeepSeekConfig.setup_environment()
        
        from langchain_openai import ChatOpenAI
        from langchain.schema import HumanMessage
        
        llm = ChatOpenAI(
            model=config["model"],
            openai_api_base=config["base_url"],
            openai_api_key=config["api_key"],
            temperature=0.7,
            max_tokens=100
        )
        
        print("🚀 Making direct API call...")
        
        response = llm.invoke([HumanMessage(content="Say hello from DeepSeek in one sentence.")])
        
        print(f"✅ Direct LLM Test Successful!")
        print(f"Response: {response.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct LLM test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Choose test type:")
    print("1. Configuration only")
    print("2. Direct LLM test")
    print("3. Full CrewAI test")
    
    choice = input("Enter choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        test_config_only()
    elif choice == "2":
        test_direct_llm()
    elif choice == "3":
        test_deepseek_connection()
    else:
        print("Invalid choice, running configuration test...")
        test_config_only()