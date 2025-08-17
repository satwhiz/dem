#!/usr/bin/env python3
"""
Working DeepSeek test script with proper LiteLLM integration
"""
import os
from dotenv import load_dotenv
from deepseek_config import DeepSeekConfig

def test_config():
    """Test configuration"""
    print("🔍 Testing Configuration")
    print("=" * 25)
    
    try:
        DeepSeekConfig.print_config()
        return True
    except Exception as e:
        print(f"❌ Config failed: {e}")
        return False

def test_direct_openai():
    """Test direct OpenAI client with DeepSeek"""
    print("\n🧪 Testing Direct OpenAI Client")
    print("=" * 30)
    
    try:
        from openai import OpenAI
        from deepseek_config import DeepSeekConfig
        
        config = DeepSeekConfig.setup_environment()
        
        client = OpenAI(
            api_key=config["api_key"],
            base_url=config["base_url"]
        )
        
        # Remove deepseek/ prefix for direct OpenAI client
        model_name = config["model"].replace("deepseek/", "")
        
        print(f"🚀 Making API call with model: {model_name}")
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "Say hello from DeepSeek in one sentence."}],
            max_tokens=50,
            temperature=0.7
        )
        
        print(f"✅ Direct API Test Successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ Direct API test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_langchain():
    """Test LangChain with DeepSeek"""
    print("\n🧪 Testing LangChain Integration")
    print("=" * 30)
    
    try:
        from langchain_openai import ChatOpenAI
        from langchain.schema import HumanMessage
        from deepseek_config import DeepSeekConfig
        
        config = DeepSeekConfig.setup_environment()
        
        # For LangChain, we need the full model name with prefix
        llm = ChatOpenAI(
            model=config["model"],  # Keep deepseek/ prefix for LangChain
            openai_api_base=config["base_url"],
            openai_api_key=config["api_key"],
            temperature=config["temperature"],
            max_tokens=50
        )
        
        print(f"🚀 Testing LangChain with model: {config['model']}")
        
        response = llm.invoke([HumanMessage(content="Say hello from DeepSeek via LangChain.")])
        
        print(f"✅ LangChain Test Successful!")
        print(f"Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ LangChain test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_crewai():
    """Test CrewAI with proper DeepSeek configuration"""
    print("\n🧪 Testing CrewAI Integration")
    print("=" * 30)
    
    try:
        from crewai import Agent, Task, Crew, Process
        from langchain_openai import ChatOpenAI
        from deepseek_config import DeepSeekConfig
        
        config = DeepSeekConfig.setup_environment()
        
        # Create LLM instance
        llm = ChatOpenAI(
            model=config["model"],
            openai_api_base=config["base_url"],
            openai_api_key=config["api_key"],
            temperature=config["temperature"],
            max_tokens=100
        )
        
        # Create agent with LLM instance
        agent = Agent(
            role='Test Agent',
            goal='Test DeepSeek API',
            backstory='You are testing the DeepSeek API integration.',
            verbose=True,
            allow_delegation=False,
            llm=llm  # Pass LLM instance directly
        )
        
        task = Task(
            description="Say hello from DeepSeek via CrewAI. Keep it to one sentence.",
            agent=agent,
            expected_output="A brief hello message"
        )
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        print(f"🚀 Testing CrewAI with model: {config['model']}")
        
        result = crew.kickoff()
        
        print(f"\n✅ CrewAI Test Successful!")
        print(f"Response: {result}")
        return True
        
    except Exception as e:
        print(f"❌ CrewAI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🧪 DeepSeek Integration Test Suite")
    print("=" * 35)
    
    tests = [
        ("Configuration", test_config),
        ("Direct OpenAI Client", test_direct_openai),
        ("LangChain", test_langchain),
        ("CrewAI", test_crewai)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print('='*50)
        
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print('='*50)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! DeepSeek is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    print("Choose test mode:")
    print("1. Run all tests")
    print("2. Configuration only")
    print("3. Direct API only")
    print("4. LangChain only") 
    print("5. CrewAI only")
    
    choice = input("Enter choice (1-5): ").strip()
    
    if choice == "1":
        main()
    elif choice == "2":
        test_config()
    elif choice == "3":
        test_direct_openai()
    elif choice == "4":
        test_langchain()
    elif choice == "5":
        test_crewai()
    else:
        print("Invalid choice, running all tests...")
        main()
