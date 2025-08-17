
import pandas as pd
import json
import os
from typing import Dict, List, Tuple, Any
from datetime import datetime
import hashlib

class TrialBalanceTools:
    
    @staticmethod
    def load_trial_balance(file_path: str) -> pd.DataFrame:
        """Load trial balance from CSV file"""
        try:
            df = pd.read_csv(file_path)
            print(f"✅ Loaded {len(df)} records from {file_path}")
            return df
        except Exception as e:
            print(f"❌ Error loading {file_path}: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def load_config(config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            print(f"✅ Loaded configuration from {config_path}")
            return config
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return {}
    
    @staticmethod
    def categorize_account(account_number: str, config: Dict) -> str:
        """Categorize account based on account number ranges"""
        account_ranges = config.get('account_ranges', {})
        
        for range_key, category in account_ranges.items():
            start, end = range_key.split('-')
            if start <= account_number <= end:
                return category
        return "Unknown"
    
    @staticmethod
    def calculate_variance(current_amount: float, prior_amount: float) -> Dict:
        """Calculate variance between periods"""
        if prior_amount == 0:
            variance_pct = 100 if current_amount != 0 else 0
        else:
            variance_pct = ((current_amount - prior_amount) / abs(prior_amount)) * 100
        
        variance_amount = current_amount - prior_amount
        
        return {
            "variance_amount": variance_amount,
            "variance_pct": variance_pct,
            "is_material": abs(variance_pct) > 15  # 15% threshold
        }
    
    @staticmethod
    def validate_trial_balance(df: pd.DataFrame) -> Dict:
        """Validate trial balance for completeness and accuracy"""
        total_debits = df['debit'].sum()
        total_credits = df['credit'].sum()
        difference = abs(total_debits - total_credits)
        
        validation_results = {
            "total_debits": total_debits,
            "total_credits": total_credits,
            "difference": difference,
            "is_balanced": difference < 0.01,  # Allow for rounding
            "missing_categories": df[df['category'].isna()].shape[0] if 'category' in df.columns else 0,
            "duplicate_accounts": df.duplicated(['account_number']).sum()
        }
        
        return validation_results
    
    @staticmethod
    def save_output(data: Any, file_path: str, format_type: str = 'json'):
        """Save processed data to output file"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        if format_type == 'json':
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        elif format_type == 'csv':
            if isinstance(data, pd.DataFrame):
                data.to_csv(file_path, index=False)
        
        print(f"✅ Saved output to {file_path}")
    
    @staticmethod
    def create_audit_log(agent_name: str, action: str, details: Dict):
        """Create audit log entry"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "agent": agent_name,
            "action": action,
            "details": details,
            "hash": hashlib.md5(str(details).encode()).hexdigest()[:8]
        }
        
        log_file = f"logs/audit_{datetime.now().strftime('%Y%m%d')}.jsonl"
        os.makedirs('logs', exist_ok=True)
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        return log_entry
