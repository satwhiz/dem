import os
import sys
import argparse
from dotenv import load_dotenv
from deepseek_config import DeepSeekConfig

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from dynamic_demo import DynamicTrialBalanceSystem

def create_test_data():
    """Create test data files with different schemas"""
    
    # Create test directory
    os.makedirs('data/test', exist_ok=True)
    
    # SAP Full Year Data
    sap_data = """gl_account,gl_description,dr_amount,cr_amount,company_code,period_ending
1000,Cash and Bank Balances,150000,0,ENT001,2024-01-31
1100,Trade Receivables,95000,0,ENT001,2024-01-31
1150,Prepaid Insurance,8000,0,ENT001,2024-01-31
1500,Raw Materials Inventory,120000,0,ENT001,2024-01-31
2000,Trade Payables,0,65000,ENT001,2024-01-31
2100,Accrued Salaries,0,25000,ENT001,2024-01-31
3000,Share Capital,0,200000,ENT001,2024-01-31
4000,Sales Revenue,0,180000,ENT001,2024-01-31
5000,Cost of Goods Sold,95000,0,ENT001,2024-01-31
5100,Employee Costs,45000,0,ENT001,2024-01-31
5200,Rent Expense,12000,0,ENT001,2024-01-31
5300,Marketing Costs,8000,0,ENT001,2024-01-31
1000,Cash and Bank Balances,140000,0,ENT001,2024-03-31
1100,Trade Receivables,125000,0,ENT001,2024-03-31
1150,Prepaid Insurance,7000,0,ENT001,2024-03-31
1500,Raw Materials Inventory,140000,0,ENT001,2024-03-31
1600,Finished Goods,25000,0,ENT001,2024-03-31
2000,Trade Payables,0,85000,ENT001,2024-03-31
2100,Accrued Salaries,0,30000,ENT001,2024-03-31
2200,Customer Advances,0,15000,ENT001,2024-03-31
3000,Share Capital,0,200000,ENT001,2024-03-31
4000,Sales Revenue,0,220000,ENT001,2024-03-31
5000,Cost of Goods Sold,125000,0,ENT001,2024-03-31
5100,Employee Costs,52000,0,ENT001,2024-03-31
5200,Rent Expense,36000,0,ENT001,2024-03-31
5300,Marketing Costs,22000,0,ENT001,2024-03-31
5400,IT Infrastructure Costs,8000,0,ENT001,2024-03-31
1000,Cash and Bank Balances,132000,0,ENT001,2024-06-30
1100,Trade Receivables,165000,0,ENT001,2024-06-30
1150,Prepaid Insurance,5500,0,ENT001,2024-06-30
1500,Raw Materials Inventory,165000,0,ENT001,2024-06-30
1600,Finished Goods,45000,0,ENT001,2024-06-30
1700,Fixed Assets,85000,0,ENT001,2024-06-30
2000,Trade Payables,0,115000,ENT001,2024-06-30
2100,Accrued Salaries,0,38000,ENT001,2024-06-30
2200,Customer Advances,0,25000,ENT001,2024-06-30
2300,Short Term Loans,0,50000,ENT001,2024-06-30
3000,Share Capital,0,200000,ENT001,2024-06-30
3100,Retained Earnings,0,55000,ENT001,2024-06-30
4000,Sales Revenue,0,380000,ENT001,2024-06-30
4100,Service Revenue,0,45000,ENT001,2024-06-30
5000,Cost of Goods Sold,220000,0,ENT001,2024-06-30
5100,Employee Costs,85000,0,ENT001,2024-06-30
5200,Rent Expense,25000,0,ENT001,2024-06-30
5300,Marketing Costs,42000,0,ENT001,2024-06-30
5400,IT Infrastructure Costs,28000,0,ENT001,2024-06-30
5500,Professional Services,15000,0,ENT001,2024-06-30"""

    with open('data/test/sap_full_year_2024.csv', 'w') as f:
        f.write(sap_data)
    
    # Oracle Q2 Data (different schema)
    oracle_data = """account_id,account_desc,debit,credit,entity,as_of_date
1000,Cash and Cash Equivalents,132000,0,ENT001,2024-06-30
1100,Accounts Receivable,165000,0,ENT001,2024-06-30
1150,Prepaid Expenses,5500,0,ENT001,2024-06-30
1500,Inventory,165000,0,ENT001,2024-06-30
1600,Finished Goods,45000,0,ENT001,2024-06-30
1700,Fixed Assets,85000,0,ENT001,2024-06-30
2000,Accounts Payable,0,115000,ENT001,2024-06-30
2100,Accrued Expenses,0,38000,ENT001,2024-06-30
2200,Deferred Revenue,0,25000,ENT001,2024-06-30
2300,Short Term Loans,0,50000,ENT001,2024-06-30
3000,Common Stock,0,200000,ENT001,2024-06-30
3100,Retained Earnings,0,55000,ENT001,2024-06-30
4000,Product Sales,0,380000,ENT001,2024-06-30
4100,Service Revenue,0,45000,ENT001,2024-06-30
5000,Cost of Sales,220000,0,ENT001,2024-06-30
5100,Salaries,85000,0,ENT001,2024-06-30
5200,Facilities,25000,0,ENT001,2024-06-30
5300,Marketing,42000,0,ENT001,2024-06-30
5400,Technology,28000,0,ENT001,2024-06-30
5500,Professional Services,15000,0,ENT001,2024-06-30"""

    with open('data/test/oracle_q2_2024.csv', 'w') as f:
        f.write(oracle_data)
    
    # 2023 Comparison Data
    comparison_data = """Account Number,Account Name,Debit Amount,Credit Amount,Company,Period End
1000,Cash and Cash Equivalents,180000,0,ENT001,2023-12-31
1100,Accounts Receivable,155000,0,ENT001,2023-12-31
1500,Inventory,145000,0,ENT001,2023-12-31
1700,Property Plant Equipment,75000,0,ENT001,2023-12-31
2000,Accounts Payable,0,95000,ENT001,2023-12-31
2100,Accrued Liabilities,0,35000,ENT001,2023-12-31
3000,Common Stock,0,200000,ENT001,2023-12-31
3100,Retained Earnings,0,85000,ENT001,2023-12-31
4000,Sales Revenue,0,580000,ENT001,2023-12-31
5000,Cost of Goods Sold,325000,0,ENT001,2023-12-31
5100,Employee Expenses,125000,0,ENT001,2023-12-31
5200,Rent and Utilities,45000,0,ENT001,2023-12-31
5300,Marketing Expenses,65000,0,ENT001,2023-12-31
5500,Administrative Expenses,25000,0,ENT001,2023-12-31"""

    with open('data/test/excel_export_2023.csv', 'w') as f:
        f.write(comparison_data)
    
    print("✅ Test data files created in data/test/")

def run_example_analyses():
    """Run several example analyses to demonstrate capabilities"""
    
    system = DynamicTrialBalanceSystem()
    
    examples = [
        {
            "request": "Analyze Q1 2024 data and identify new accounts",
            "files": ["data/test/sap_full_year_2024.csv"],
            "labels": ["SAP_Data"]
        },
        {
            "request": "Compare Q2 2024 performance vs 2023 full year",
            "files": ["data/test/oracle_q2_2024.csv", "data/test/excel_export_2023.csv"],
            "labels": ["Q2_2024", "Full_Year_2023"]
        },
        {
            "request": "Check for variance in cash and receivables between Q1 and Q2 2024",
            "files": ["data/test/sap_full_year_2024.csv", "data/test/oracle_q2_2024.csv"],
            "labels": ["SAP_Full_Year", "Oracle_Q2"]
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{'='*60}")
        print(f"EXAMPLE {i}: {example['request']}")
        print('='*60)
        
        try:
            result = system.run_analysis(
                example["request"],
                example["files"], 
                example["labels"]
            )
            
            if result:
                print(f"✅ Example {i} completed successfully!")
            else:
                print(f"❌ Example {i} failed")
                
        except Exception as e:
            print(f"❌ Example {i} error: {e}")

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='Dynamic Trial Balance Analysis System')
    parser.add_argument('--create-test-data', action='store_true', 
                       help='Create test data files with different schemas')
    parser.add_argument('--run-examples', action='store_true',
                       help='Run example analyses')
    parser.add_argument('--interactive', action='store_true',
                       help='Start interactive mode')
    parser.add_argument('--request', type=str,
                       help='Analysis request (e.g., "Analyze Q1 2024 for new accounts")')
    parser.add_argument('--files', type=str, nargs='+',
                       help='Data files to analyze')
    parser.add_argument('--labels', type=str, nargs='+',
                       help='Labels for the data files')
    
    args = parser.parse_args()
    
    # Check for API key
    load_dotenv()
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OpenAI API key not found. Please set OPENAI_API_KEY in .env file")
        return 1
    
    if args.create_test_data:
        create_test_data()
        return 0
    
    if args.run_examples:
        run_example_analyses()
        return 0
    
    if args.request and args.files:
        system = DynamicTrialBalanceSystem()
        result = system.run_analysis(args.request, args.files, args.labels)
        return 0 if result else 1
    
    if args.interactive:
        # Import and run the interactive system
        from dynamic_demo import main as interactive_main
        interactive_main()
        return 0
    
    # Show help if no arguments
    parser.print_help()
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)


def example_usage_scenarios():
    """
    Example usage scenarios for the Dynamic Trial Balance System
    """
    
    examples = {
        "Quarterly Analysis": {
            "command": "python cli_demo.py --request 'Analyze Q1 2024 performance and identify new accounts' --files data/test/sap_full_year_2024.csv",
            "description": "Analyzes Q1 2024 data from SAP export, automatically filters to Q1 period"
        },
        
        "Multi-System Comparison": {
            "command": "python cli_demo.py --request 'Compare cash flow between SAP and Oracle systems for Q2 2024' --files data/test/sap_full_year_2024.csv data/test/oracle_q2_2024.csv --labels SAP_System Oracle_System",
            "description": "Compares data from different ERP systems with different schemas"
        },
        
        "Year-over-Year Variance": {
            "command": "python cli_demo.py --request 'Calculate variance in operating expenses between 2023 and Q2 2024' --files data/test/excel_export_2023.csv data/test/oracle_q2_2024.csv",
            "description": "Compares different periods and identifies material variances"
        },
        
        "Missing Account Detection": {
            "command": "python cli_demo.py --request 'Identify missing accounts in Q1 vs Q2 2024' --files data/test/sap_full_year_2024.csv",
            "description": "Detects accounts that appear in some periods but not others"
        },
        
        "Interactive Mode": {
            "command": "python cli_demo.py --interactive",
            "description": "Starts interactive mode where you can type requests and specify files dynamically"
        }
    }
    
    print("🎯 Dynamic Trial Balance System - Usage Examples")
    print("=" * 60)
    
    for scenario, details in examples.items():
        print(f"\n📋 {scenario}:")
        print(f"   Description: {details['description']}")
        print(f"   Command: {details['command']}")
    
    print(f"\n🚀 Getting Started:")
    print(f"   1. Create test data: python cli_demo.py --create-test-data")
    print(f"   2. Run examples: python cli_demo.py --run-examples") 
    print(f"   3. Try interactive mode: python cli_demo.py --interactive")


def quick_start():
    """Quick start script to set up and run a demo"""
    
    print("🚀 Dynamic Trial Balance System - Quick Start")
    print("=" * 50)
    
    # Check environment
    load_dotenv()
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OpenAI API key not found")
        print("   Please add OPENAI_API_KEY to your .env file")
        return
    
    # Create test data
    print("\n1️⃣  Creating test data...")
    create_test_data()
    
    # Initialize system
    print("\n2️⃣  Initializing analysis system...")
    system = DynamicTrialBalanceSystem()
    
    # Run a quick demo
    print("\n3️⃣  Running quick demo analysis...")
    
    request = "Analyze Q1 2024 data for new accounts and material variances"
    files = ["data/test/sap_full_year_2024.csv"]
    labels = ["SAP_Q1_Analysis"]
    
    print(f"   Request: {request}")
    print(f"   Data file: {files[0]}")
    
    try:
        result = system.run_analysis(request, files, labels)
        
        if result:
            print("\n🎉 Quick start completed successfully!")
            print("   Check data/output/ for detailed results")
            print("\n📝 Next steps:")
            print("   - Try: python cli_demo.py --interactive")
            print("   - Or: python cli_demo.py --run-examples")
        else:
            print("\n❌ Quick start failed")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    quick_start()