import os
import pandas as pd
from dotenv import load_dotenv

def verify_setup():
    print("🔍 Verifying Trial Balance Demo Setup...")
    
    # Check environment
    load_dotenv()
    if os.getenv('OPENAI_API_KEY'):
        print("✅ OpenAI API key found")
    else:
        print("❌ OpenAI API key missing")
        return False
    
    # Check data files
    files_to_check = [
        'data/reference/trial_balance_2023.csv',
        'data/input/trial_balance_2024.csv', 
        'src/config/account_mapping.json'
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    # Test pandas read
    try:
        df_2024 = pd.read_csv('data/input/trial_balance_2024.csv')
        df_2023 = pd.read_csv('data/reference/trial_balance_2023.csv')
        print(f"✅ Data files readable - 2024: {len(df_2024)} rows, 2023: {len(df_2023)} rows")
    except Exception as e:
        print(f"❌ Error reading data files: {e}")
        return False
    
    # Test imports
    try:
        import crewai
        import langchain
        print(f"✅ CrewAI version: {crewai.__version__}")
        print(f"✅ LangChain imported successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    print("\n🎉 Setup verification complete!")
    print("📁 Project structure ready")
    print("📊 Demo data prepared")
    print("🔧 Dependencies installed")
    return True

if __name__ == "__main__":
    verify_setup()