import os

def create_test_data():
    """Create test data files with different schemas"""
    
    print("📂 Creating test data files...")
    
    # Create test directory
    os.makedirs('data/test', exist_ok=True)
    
    # SAP Full Year Data with quarterly periods
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
1000,Cash and Bank Balances,145000,0,ENT001,2024-02-29
1100,Trade Receivables,110000,0,ENT001,2024-02-29
1150,Prepaid Insurance,7500,0,ENT001,2024-02-29
1500,Raw Materials Inventory,135000,0,ENT001,2024-02-29
2000,Trade Payables,0,72000,ENT001,2024-02-29
2100,Accrued Salaries,0,28000,ENT001,2024-02-29
3000,Share Capital,0,200000,ENT001,2024-02-29
4000,Sales Revenue,0,195000,ENT001,2024-02-29
5000,Cost of Goods Sold,105000,0,ENT001,2024-02-29
5100,Employee Costs,48000,0,ENT001,2024-02-29
5200,Rent Expense,24000,0,ENT001,2024-02-29
5300,Marketing Costs,15000,0,ENT001,2024-02-29
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
1000,Cash and Bank Balances,135000,0,ENT001,2024-04-30
1100,Trade Receivables,140000,0,ENT001,2024-04-30
1150,Prepaid Insurance,6500,0,ENT001,2024-04-30
1500,Raw Materials Inventory,150000,0,ENT001,2024-04-30
1600,Finished Goods,30000,0,ENT001,2024-04-30
2000,Trade Payables,0,95000,ENT001,2024-04-30
2100,Accrued Salaries,0,32000,ENT001,2024-04-30
2200,Customer Advances,0,20000,ENT001,2024-04-30
3000,Share Capital,0,200000,ENT001,2024-04-30
4000,Sales Revenue,0,240000,ENT001,2024-04-30
5000,Cost of Goods Sold,140000,0,ENT001,2024-04-30
5100,Employee Costs,55000,0,ENT001,2024-04-30
5200,Rent Expense,48000,0,ENT001,2024-04-30
5300,Marketing Costs,28000,0,ENT001,2024-04-30
5400,IT Infrastructure Costs,15000,0,ENT001,2024-04-30
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
    print("✅ Created: data/test/sap_full_year_2024.csv")
    
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
    print("✅ Created: data/test/oracle_q2_2024.csv")
    
    # 2023 Comparison Data (Excel export format)
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
    print("✅ Created: data/test/excel_export_2023.csv")
    
    # Q1 only data for testing period filtering
    q1_data = """account_code,acc_name,debit_amt,credit_amt,org_id,date
1000,Cash,135000,0,ENT001,2024-03-31
1100,Receivables,98000,0,ENT001,2024-03-31
1500,Stock,155000,0,ENT001,2024-03-31
2000,Payables,0,78000,ENT001,2024-03-31
2100,Accruals,0,32000,ENT001,2024-03-31
3000,Capital,0,200000,ENT001,2024-03-31
4000,Sales,0,285000,ENT001,2024-03-31
5000,COGS,165000,0,ENT001,2024-03-31
5100,Wages,68000,0,ENT001,2024-03-31
5200,Overheads,42000,0,ENT001,2024-03-31"""

    with open('data/test/q1_only_2024.csv', 'w') as f:
        f.write(q1_data)
    print("✅ Created: data/test/q1_only_2024.csv")
    
    print(f"\n🎉 Test data creation complete!")
    print(f"📁 Created 4 test files in data/test/ directory")
    print(f"📊 Each file has different schema to test auto-detection")

def verify_data():
    """Verify the test data was created correctly"""
    import pandas as pd
    
    files = [
        'data/test/sap_full_year_2024.csv',
        'data/test/oracle_q2_2024.csv', 
        'data/test/excel_export_2023.csv',
        'data/test/q1_only_2024.csv'
    ]
    
    print("\n🔍 Verifying test data...")
    
    for file_path in files:
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                print(f"✅ {file_path}: {len(df)} rows, {len(df.columns)} columns")
                print(f"   Columns: {list(df.columns)}")
            except Exception as e:
                print(f"❌ Error reading {file_path}: {e}")
        else:
            print(f"❌ Missing: {file_path}")

def main():
    """Main function"""
    print("🚀 Test Data Setup for Dynamic Trial Balance System")
    print("=" * 55)
    
    create_test_data()
    verify_data()
    
    print(f"\n📝 Next steps:")
    print(f"   1. Run: python simple_demo.py (for basic demo)")
    print(f"   2. Try: python dynamic_demo.py (if you have the dynamic system)")
    print(f"   3. Or check the data files manually in data/test/")

if __name__ == "__main__":
    main()