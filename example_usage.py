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