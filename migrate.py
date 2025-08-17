# =============================================================================
# File: migrate_to_deepseek.py - Automatic Migration Script
# =============================================================================

import os
import shutil
from datetime import datetime

def backup_files():
    """Create backup of existing files before migration"""
    backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    files_to_backup = [
        '.env',
        'simple_demo.py',
        'dynamic_demo.py',
        'quick_start.py'
    ]
    
    print(f"📦 Creating backup in {backup_dir}/")
    for file in files_to_backup:
        if os.path.exists(file):
            shutil.copy2(file, f"{backup_dir}/{file}")
            print(f"   ✅ Backed up {file}")
    
    return backup_dir

def update_env_file():
    """Update .env file for DeepSeek"""
    print("\n🔧 Updating .env file...")
    
    # Read existing .env if it exists
    existing_key = ""
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    existing_key = line.strip()
                    break
    
    new_env_content = f"""# DeepSeek API Configuration
{existing_key if existing_key else "OPENAI_API_KEY=your_deepseek_api_key_here"}
OPENAI_API_BASE=https://api.deepseek.com
OPENAI_MODEL_NAME=deepseek-chat

# Available DeepSeek Models:
# deepseek-chat - General purpose conversational model (recommended)
# deepseek-coder - Optimized for coding tasks  
# deepseek-reasoner - Enhanced reasoning capabilities

# Optional parameters
DEEPSEEK_TEMPERATURE=0.7
DEEPSEEK_MAX_TOKENS=4000
"""
    
    with open('.env', 'w') as f:
        f.write(new_env_content)
    
    print("   ✅ Updated .env file with DeepSeek configuration")

def create_deepseek_config():
    """Create DeepSeek configuration helper"""
    print("\n🔧 Creating deepseek_config.py...")
    
    config_content = '''import os
from dotenv import load_dotenv

class DeepSeekConfig:
    """Configuration for DeepSeek API integration"""
    
    @staticmethod
    def setup_environment():
        """Setup environment variables for DeepSeek"""
        load_dotenv()
        
        # Set the base URL for DeepSeek
        os.environ["OPENAI_API_BASE"] = "https://api.deepseek.com"
        
        # Default model
        if not os.getenv("OPENAI_MODEL_NAME"):
            os.environ["OPENAI_MODEL_NAME"] = "deepseek-chat"
        
        # Validate API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        return {
            "api_key": api_key,
            "base_url": os.getenv("OPENAI_API_BASE", "https://api.deepseek.com"),
            "model": os.getenv("OPENAI_MODEL_NAME", "deepseek-chat"),
            "temperature": float(os.getenv("DEEPSEEK_TEMPERATURE", "0.7")),
            "max_tokens": int(os.getenv("DEEPSEEK_MAX_TOKENS", "4000"))
        }
    
    @staticmethod
    def get_model_config():
        """Get model configuration for CrewAI"""
        config = DeepSeekConfig.setup_environment()
        
        return {
            "model": config["model"],
            "base_url": config["base_url"],
            "api_key": config["api_key"],
            "temperature": config["temperature"],
            "max_tokens": config["max_tokens"]
        }
    
    @staticmethod
    def print_config():
        """Print current configuration for debugging"""
        try:
            config = DeepSeekConfig.setup_environment()
            print("🔍 DeepSeek Configuration:")
            print(f"   Model: {config['model']}")
            print(f"   Base URL: {config['base_url']}")
            print(f"   API Key: {config['api_key'][:8]}..." if config['api_key'] else "   API Key: Not set")
            print(f"   Temperature: {config['temperature']}")
            print(f"   Max Tokens: {config['max_tokens']}")
        except Exception as e:
            print(f"❌ Configuration error: {e}")
'''
    
    with open('deepseek_config.py', 'w') as f:
        f.write(config_content)
    
    print("   ✅ Created deepseek_config.py")

def update_simple_demo():
    """Update simple_demo.py for DeepSeek"""
    print("\n🔧 Updating simple_demo.py...")
    
    if not os.path.exists('simple_demo.py'):
        print("   ⚠️  simple_demo.py not found, skipping...")
        return
    
    # Read existing file
    with open('simple_demo.py', 'r') as f:
        content = f.read()
    
    # Add DeepSeek import if not present
    if 'from deepseek_config import DeepSeekConfig' not in content:
        # Find the imports section and add DeepSeek import
        lines = content.split('\n')
        insert_index = 0
        
        for i, line in enumerate(lines):
            if line.startswith('from') or line.startswith('import'):
                insert_index = i + 1
        
        lines.insert(insert_index, 'from deepseek_config import DeepSeekConfig')
        content = '\n'.join(lines)
    
    # Update the agent creation to include DeepSeek config
    old_agent_pattern = '''data_analyst = Agent(
            role='Senior Financial Data Analyst',
            goal='Analyze trial balance data and provide insights',
            backstory="""You are a senior financial analyst with 15+ years of experience 
            in trial balance processing, variance analysis, and tax provision preparation. 
            You have expertise in identifying new accounts, material variances, and ensuring data quality.""",
            verbose=True,
            allow_delegation=False
        )'''
    
    new_agent_pattern = '''# Setup DeepSeek configuration
        config = DeepSeekConfig.get_model_config()
        print(f"🤖 Using DeepSeek model: {config['model']}")
        
        data_analyst = Agent(
            role='Senior Financial Data Analyst',
            goal='Analyze trial balance data and provide insights',
            backstory="""You are a senior financial analyst with 15+ years of experience 
            in trial balance processing, variance analysis, and tax provision preparation. 
            You have expertise in identifying new accounts, material variances, and ensuring data quality.""",
            verbose=True,
            allow_delegation=False,
            llm_config={
                "model": config["model"],
                "base_url": config["base_url"],
                "api_key": config["api_key"],
                "temperature": config["temperature"]
            }
        )'''
    
    # Replace the agent creation
    content = content.replace(old_agent_pattern, new_agent_pattern)
    
    # Write updated content
    with open('simple_demo.py', 'w') as f:
        f.write(content)
    
    print("   ✅ Updated simple_demo.py with DeepSeek configuration")

def create_test_script():
    """Create DeepSeek test script"""
    print("\n🔧 Creating test_deepseek.py...")
    
    test_content = '''#!/usr/bin/env python3
"""
Test script for DeepSeek API integration
"""
import os
from dotenv import load_dotenv
from deepseek_config import DeepSeekConfig

def test_deepseek_connection():
    """Test DeepSeek API connection"""
    print("🧪 Testing DeepSeek API Connection")
    print("=" * 40)
    
    try:
        # Setup configuration
        config = DeepSeekConfig.setup_environment()
        print(f"✅ Configuration loaded:")
        print(f"   Model: {config['model']}")
        print(f"   Base URL: {config['base_url']}")
        print(f"   API Key: {config['api_key'][:8]}..." if config['api_key'] else "   API Key: Not set")
        
        # Test with a simple CrewAI agent
        from crewai import Agent, Task, Crew, Process
        
        test_agent = Agent(
            role='Test Agent',
            goal='Test DeepSeek API connection',
            backstory='You are a test agent to verify API connectivity.',
            verbose=True,
            allow_delegation=False,
            llm_config={
                "model": config["model"],
                "base_url": config["base_url"],
                "api_key": config["api_key"],
                "temperature": config["temperature"]
            }
        )
        
        test_task = Task(
            description="Say hello and confirm you are working with DeepSeek API. Keep it brief.",
            agent=test_agent,
            expected_output="A brief hello message confirming DeepSeek connectivity"
        )
        
        test_crew = Crew(
            agents=[test_agent],
            tasks=[test_task],
            process=Process.sequential,
            verbose=True
        )
        
        print("\\n🚀 Testing API call...")
        result = test_crew.kickoff()
        
        print(f"\\n✅ DeepSeek API Test Successful!")
        print(f"Response: {result}")
        
        return True
        
    except Exception as e:
        print(f"\\n❌ DeepSeek API Test Failed: {e}")
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

if __name__ == "__main__":
    print("Choose test type:")
    print("1. Configuration only")
    print("2. Full API test")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_config_only()
    elif choice == "2":
        test_deepseek_connection()
    else:
        print("Invalid choice, running configuration test...")
        test_config_only()
'''
    
    with open('test_deepseek.py', 'w') as f:
        f.write(test_content)
    
    print("   ✅ Created test_deepseek.py")

def main():
    """Main migration function"""
    print("🚀 DeepSeek Migration Script")
    print("=" * 30)
    print("This script will update your trial balance system to use DeepSeek API")
    print()
    
    # Confirm migration
    confirm = input("Do you want to proceed? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Migration cancelled.")
        return
    
    # Create backup
    backup_dir = backup_files()
    
    # Perform migration steps
    update_env_file()
    create_deepseek_config()
    update_simple_demo()
    create_test_script()
    
    print(f"\\n🎉 Migration Complete!")
    print(f"📦 Backup created in: {backup_dir}/")
    print()
    print("📝 Next steps:")
    print("1. Update your DeepSeek API key in .env file:")
    print("   OPENAI_API_KEY=your_deepseek_api_key_here")
    print()
    print("2. Test the configuration:")
    print("   python test_deepseek.py")
    print()
    print("3. Run your demo:")
    print("   python simple_demo.py")
    print()
    print("⚠️  Remember to:")
    print("   - Get your DeepSeek API key from https://platform.deepseek.com/")
    print("   - Update the API key in .env file")
    print("   - Test the connection before running full demos")

if __name__ == "__main__":
    main()
    
    with open('migrate_to_deepseek.py', 'w') as f:
        f.write(migration_script)