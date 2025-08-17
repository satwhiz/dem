"""
Trial Balance Automation Demo Runner
"""
import os
import sys
from datetime import datetime

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
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OpenAI API key not found in environment")
        return False
    print("✅ OpenAI API key configured")
    
    return True

def main():
    """Run the trial balance automation demo"""
    print("🎬 Trial Balance Automation Demo")
    print("=" * 50)
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please check setup.")
        return 1
    
    print("\n🚀 Launching CrewAI Trial Balance Automation...")
    print("=" * 50)
    
    try:
        from src.main_demo import TrialBalanceDemo
        
        demo = TrialBalanceDemo()
        results = demo.run_demo()
        
        print("\n🎉 Demo completed successfully!")
        print(f"🕒 Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)