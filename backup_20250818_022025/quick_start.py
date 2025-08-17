# =============================================================================
# File: quick_start.py - Fixed Quick Start Script
# =============================================================================

import os
import sys
from dotenv import load_dotenv

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

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
    
    try:
        from dynamic_demo import DynamicTrialBalanceSystem
        system = DynamicTrialBalanceSystem()
    except ImportError as e:
        print(f"❌ Error importing dynamic_demo: {e}")
        print("   Please make sure dynamic_demo.py is in the current directory")
        return
    
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
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    quick_start()