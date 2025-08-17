# =============================================================================
# File: src/tools/crew_tools.py (UPDATED VERSION)
# =============================================================================

from crewai.tools import tool
import pandas as pd
import json
import os

@tool
def load_trial_balance(file_path: str) -> str:
    """
    Load and validate trial balance data from CSV file.
    
    Args:
        file_path (str): Path to the trial balance CSV file
        
    Returns:
        str: JSON summary of loaded trial balance data
    """
    try:
        df = pd.read_csv(file_path)
        # Basic validation
        required_columns = ['account_number', 'account_name', 'debit', 'credit']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return f"Error: Missing required columns: {missing_columns}"
        
        # Calculate net balances
        df['net_balance'] = df['debit'] - df['credit']
        
        summary = {
            "total_records": len(df),
            "total_debits": float(df['debit'].sum()),
            "total_credits": float(df['credit'].sum()),
            "balance_difference": float(df['debit'].sum() - df['credit'].sum()),
            "sample_accounts": df[['account_number', 'account_name', 'net_balance']].head(10).to_dict('records')
        }
        
        return json.dumps(summary, indent=2)
        
    except Exception as e:
        return f"Error loading trial balance: {str(e)}"

@tool
def categorize_account(account_number: str, account_name: str) -> str:
    """
    Categorize account based on account number and mapping rules.
    
    Args:
        account_number (str): Account number to categorize
        account_name (str): Account name for context
        
    Returns:
        str: JSON result with categorization details
    """
    try:
        # Load mapping configuration
        config_path = 'src/config/account_mapping.json'
        if not os.path.exists(config_path):
            return f"Error: Configuration file not found at {config_path}"
            
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Determine category based on account number
        account_ranges = config.get('account_ranges', {})
        category = "Unknown"
        
        for range_key, cat in account_ranges.items():
            start, end = range_key.split('-')
            if start <= account_number <= end:
                category = cat
                break
        
        # Determine tax category
        tax_categories = config.get('tax_categories', {})
        tax_category = "Standard"
        
        if category in tax_categories:
            # Simple logic for demo - use first tax category
            tax_category = tax_categories[category][0]
        
        result = {
            "account_number": account_number,
            "account_name": account_name,
            "category": category,
            "tax_category": tax_category,
            "confidence": 0.95 if category != "Unknown" else 0.3,
            "reasoning": f"Account {account_number} falls in range for {category} accounts"
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return f"Error categorizing account: {str(e)}"

@tool
def variance_analysis(current_file: str, prior_file: str) -> str:
    """
    Compare trial balances between periods and identify variances.
    
    Args:
        current_file (str): Current period trial balance file
        prior_file (str): Prior period trial balance file
        
    Returns:
        str: JSON result with variance analysis
    """
    try:
        # Check if files exist
        if not os.path.exists(current_file):
            return f"Error: Current file not found: {current_file}"
        if not os.path.exists(prior_file):
            return f"Error: Prior file not found: {prior_file}"
            
        # Load both periods
        current_df = pd.read_csv(current_file)
        prior_df = pd.read_csv(prior_file)
        
        # Calculate net balances
        current_df['net_balance'] = current_df['debit'] - current_df['credit']
        prior_df['net_balance'] = prior_df['debit'] - prior_df['credit']
        
        # Merge on account number
        comparison = current_df.merge(
            prior_df[['account_number', 'net_balance']], 
            on='account_number', 
            how='outer', 
            suffixes=('_current', '_prior')
        ).fillna(0)
        
        # Calculate variances
        comparison['variance_amount'] = comparison['net_balance_current'] - comparison['net_balance_prior']
        comparison['variance_pct'] = comparison.apply(
            lambda row: 0 if row['net_balance_prior'] == 0 
            else (row['variance_amount'] / abs(row['net_balance_prior'])) * 100, 
            axis=1
        )
        
        # Flag material variances (>15%)
        material_variances = comparison[abs(comparison['variance_pct']) > 15]
        
        # New accounts (in current but not prior)
        new_accounts = comparison[comparison['net_balance_prior'] == 0]
        new_accounts = new_accounts[new_accounts['net_balance_current'] != 0]
        
        result = {
            "total_accounts_current": len(current_df),
            "total_accounts_prior": len(prior_df),
            "material_variances_count": len(material_variances),
            "new_accounts_count": len(new_accounts),
            "variance_details": material_variances[
                ['account_number', 'account_name', 'net_balance_current', 
                 'net_balance_prior', 'variance_amount', 'variance_pct']
            ].to_dict('records'),
            "new_account_details": new_accounts[
                ['account_number', 'account_name', 'net_balance_current']
            ].to_dict('records')
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return f"Error in variance analysis: {str(e)}"

@tool
def validate_compliance(data_summary: str) -> str:
    """
    Validate trial balance for compliance and data integrity.
    
    Args:
        data_summary (str): Summary of processed trial balance data
        
    Returns:
        str: JSON result with compliance validation
    """
    try:
        # For demo purposes, we'll load the current file directly
        current_file = "data/input/trial_balance_2024.csv"
        
        if not os.path.exists(current_file):
            return f"Error: Current trial balance file not found: {current_file}"
        
        df = pd.read_csv(current_file)
        
        # Perform validation checks
        total_debits = df['debit'].sum()
        total_credits = df['credit'].sum()
        difference = abs(total_debits - total_credits)
        
        # Check for missing data
        missing_account_numbers = df['account_number'].isna().sum()
        missing_account_names = df['account_name'].isna().sum()
        duplicate_accounts = df.duplicated(['account_number']).sum()
        
        # Compliance results
        validation_results = {
            "total_debits": float(total_debits),
            "total_credits": float(total_credits),
            "balance_difference": float(difference),
            "is_balanced": difference < 0.01,
            "missing_account_numbers": int(missing_account_numbers),
            "missing_account_names": int(missing_account_names), 
            "duplicate_accounts": int(duplicate_accounts),
            "total_accounts": len(df),
            "compliance_status": "PASSED" if (difference < 0.01 and missing_account_numbers == 0 and duplicate_accounts == 0) else "FAILED",
            "validation_timestamp": pd.Timestamp.now().isoformat()
        }
        
        return json.dumps(validation_results, indent=2)
        
    except Exception as e:
        return f"Error in compliance validation: {str(e)}"

@tool  
def prepare_upload_format(validation_results: str) -> str:
    """
    Prepare validated trial balance data for upload to tax provision systems.
    
    Args:
        validation_results (str): Results from compliance validation
        
    Returns:
        str: JSON formatted data ready for tax provision upload
    """
    try:
        # Load current trial balance for formatting
        current_file = "data/input/trial_balance_2024.csv"
        
        if not os.path.exists(current_file):
            return f"Error: Current trial balance file not found: {current_file}"
        
        df = pd.read_csv(current_file)
        
        # Create output directory
        output_dir = "data/output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Format for tax provision system
        tax_provision_data = {
            "entity_id": "ENT001",
            "period_end": "2024-12-31",
            "currency": "USD",
            "total_debits": float(df['debit'].sum()),
            "total_credits": float(df['credit'].sum()),
            "account_details": []
        }
        
        # Process each account
        for _, row in df.iterrows():
            account_detail = {
                "account_number": str(row['account_number']),
                "account_name": str(row['account_name']),
                "debit_amount": float(row['debit']),
                "credit_amount": float(row['credit']),
                "net_balance": float(row['debit'] - row['credit']),
                "source_system": row.get('source_system', 'SAP')
            }
            tax_provision_data["account_details"].append(account_detail)
        
        # Save formatted data
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{output_dir}/tax_provision_upload_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump(tax_provision_data, f, indent=2)
        
        upload_summary = {
            "status": "SUCCESS",
            "output_file": output_file,
            "total_accounts": len(df),
            "total_debits": float(df['debit'].sum()),
            "total_credits": float(df['credit'].sum()),
            "upload_ready": True,
            "timestamp": timestamp
        }
        
        return json.dumps(upload_summary, indent=2)
        
    except Exception as e:
        return f"Error preparing upload format: {str(e)}"