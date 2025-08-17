# =============================================================================
# File: dynamic_demo.py - Enhanced User-Driven System
# =============================================================================

import os
import sys
import pandas as pd
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Dict, List, Optional, Any
import re

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

class DataSchemaMapper:
    """Maps different CSV schemas to a standardized format"""
    
    STANDARD_SCHEMA = {
        'account_number': 'account_number',
        'account_name': 'account_name', 
        'debit': 'debit',
        'credit': 'credit',
        'period': 'period',
        'entity_id': 'entity_id'
    }
    
    # Common variations in column names
    COLUMN_MAPPINGS = {
        'account_number': ['account_no', 'acc_no', 'account_id', 'gl_account', 'account_code'],
        'account_name': ['account_desc', 'description', 'acc_name', 'gl_description', 'account_description'],
        'debit': ['debit_amount', 'dr', 'debit_amt', 'dr_amount'],
        'credit': ['credit_amount', 'cr', 'credit_amt', 'cr_amount'],
        'period': ['period_end', 'date', 'period_ending', 'as_of_date', 'reporting_date'],
        'entity_id': ['entity', 'company_id', 'legal_entity', 'company_code', 'org_id']
    }
    
    @classmethod
    def detect_schema(cls, df: pd.DataFrame) -> Dict[str, str]:
        """Automatically detect column mapping for a DataFrame"""
        columns = [col.lower().strip() for col in df.columns]
        mapping = {}
        
        for standard_col, variations in cls.COLUMN_MAPPINGS.items():
            found = False
            
            # First try exact match
            if standard_col in columns:
                mapping[standard_col] = df.columns[columns.index(standard_col)]
                found = True
            
            # Then try variations
            if not found:
                for variation in variations:
                    if variation in columns:
                        mapping[standard_col] = df.columns[columns.index(variation)]
                        found = True
                        break
            
            # Finally try partial matches
            if not found:
                for col in df.columns:
                    col_lower = col.lower()
                    if any(var in col_lower for var in variations):
                        mapping[standard_col] = col
                        found = True
                        break
        
        return mapping
    
    @classmethod
    def standardize_dataframe(cls, df: pd.DataFrame, mapping: Dict[str, str] = None) -> pd.DataFrame:
        """Convert DataFrame to standard schema"""
        if mapping is None:
            mapping = cls.detect_schema(df)
        
        standardized = df.copy()
        
        # Rename columns to standard names
        rename_map = {v: k for k, v in mapping.items() if v in df.columns}
        standardized = standardized.rename(columns=rename_map)
        
        # Ensure required columns exist with defaults
        required_columns = ['account_number', 'account_name', 'debit', 'credit']
        for col in required_columns:
            if col not in standardized.columns:
                if col in ['debit', 'credit']:
                    standardized[col] = 0.0
                else:
                    standardized[col] = 'Unknown'
        
        # Clean and convert data types
        if 'debit' in standardized.columns:
            standardized['debit'] = pd.to_numeric(standardized['debit'], errors='coerce').fillna(0)
        if 'credit' in standardized.columns:
            standardized['credit'] = pd.to_numeric(standardized['credit'], errors='coerce').fillna(0)
        
        return standardized

class PeriodFilter:
    """Handles period-based filtering of financial data"""
    
    @staticmethod
    def parse_period_request(period_text: str) -> Dict[str, Any]:
        """Parse user period requests like 'Q1 2024', 'Jan 2024', '2024', etc."""
        period_text = period_text.upper().strip()
        
        # Extract year
        year_match = re.search(r'20\d{2}', period_text)
        if not year_match:
            raise ValueError(f"Could not extract year from: {period_text}")
        year = int(year_match.group())
        
        # Determine period type and range
        if 'Q1' in period_text:
            return {
                'type': 'quarter',
                'quarter': 1,
                'year': year,
                'start_date': f'{year}-01-01',
                'end_date': f'{year}-03-31',
                'description': f'Q1 {year}'
            }
        elif 'Q2' in period_text:
            return {
                'type': 'quarter',
                'quarter': 2,
                'year': year,
                'start_date': f'{year}-04-01',
                'end_date': f'{year}-06-30',
                'description': f'Q2 {year}'
            }
        elif 'Q3' in period_text:
            return {
                'type': 'quarter',
                'quarter': 3,
                'year': year,
                'start_date': f'{year}-07-01',
                'end_date': f'{year}-09-30',
                'description': f'Q3 {year}'
            }
        elif 'Q4' in period_text:
            return {
                'type': 'quarter',
                'quarter': 4,
                'year': year,
                'start_date': f'{year}-10-01',
                'end_date': f'{year}-12-31',
                'description': f'Q4 {year}'
            }
        elif any(month in period_text for month in ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 
                                                   'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']):
            # Monthly periods
            months = {
                'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
                'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12
            }
            month_name = next(m for m in months.keys() if m in period_text)
            month_num = months[month_name]
            
            # Calculate last day of month
            if month_num == 12:
                last_day = 31
            elif month_num in [4, 6, 9, 11]:
                last_day = 30
            elif month_num == 2:
                last_day = 29 if year % 4 == 0 else 28
            else:
                last_day = 31
                
            return {
                'type': 'month',
                'month': month_num,
                'year': year,
                'start_date': f'{year}-{month_num:02d}-01',
                'end_date': f'{year}-{month_num:02d}-{last_day}',
                'description': f'{month_name} {year}'
            }
        else:
            # Full year
            return {
                'type': 'year',
                'year': year,
                'start_date': f'{year}-01-01',
                'end_date': f'{year}-12-31',
                'description': f'Full Year {year}'
            }
    
    @staticmethod
    def filter_dataframe_by_period(df: pd.DataFrame, period_info: Dict[str, Any]) -> pd.DataFrame:
        """Filter DataFrame based on period information"""
        if 'period' not in df.columns:
            print("⚠️  No period column found, returning full dataset")
            return df
        
        # Convert period column to datetime
        df_copy = df.copy()
        df_copy['period_date'] = pd.to_datetime(df_copy['period'], errors='coerce')
        
        # Filter by date range
        start_date = pd.to_datetime(period_info['start_date'])
        end_date = pd.to_datetime(period_info['end_date'])
        
        filtered_df = df_copy[
            (df_copy['period_date'] >= start_date) & 
            (df_copy['period_date'] <= end_date)
        ]
        
        # Drop the temporary column
        filtered_df = filtered_df.drop('period_date', axis=1)
        
        print(f"📅 Filtered to {period_info['description']}: {len(filtered_df)} records")
        return filtered_df

class DynamicTrialBalanceSystem:
    """Enhanced system that handles user-driven analysis"""
    
    def __init__(self):
        self.schema_mapper = DataSchemaMapper()
        self.period_filter = PeriodFilter()
        self.loaded_datasets = {}
        
    def load_user_data(self, file_paths: List[str], labels: List[str] = None) -> Dict[str, pd.DataFrame]:
        """Load multiple user data files with automatic schema detection"""
        if labels is None:
            labels = [f"dataset_{i+1}" for i in range(len(file_paths))]
        
        datasets = {}
        
        for i, file_path in enumerate(file_paths):
            label = labels[i]
            
            print(f"\n📂 Loading {label}: {file_path}")
            
            try:
                # Load the file
                if file_path.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                else:
                    df = pd.read_csv(file_path)
                
                print(f"   📊 Raw data: {len(df)} rows, {len(df.columns)} columns")
                print(f"   📋 Columns: {list(df.columns)}")
                
                # Detect and apply schema mapping
                mapping = self.schema_mapper.detect_schema(df)
                print(f"   🔗 Schema mapping: {mapping}")
                
                standardized_df = self.schema_mapper.standardize_dataframe(df, mapping)
                print(f"   ✅ Standardized: {len(standardized_df)} rows")
                
                datasets[label] = standardized_df
                
            except Exception as e:
                print(f"   ❌ Error loading {file_path}: {e}")
                continue
        
        self.loaded_datasets = datasets
        return datasets
    
    def process_user_request(self, request: str, datasets: Dict[str, pd.DataFrame] = None) -> str:
        """Process natural language requests from users"""
        if datasets is None:
            datasets = self.loaded_datasets
        
        print(f"\n🎯 Processing request: {request}")
        
        # Parse the request for period information
        period_info = None
        try:
            # Look for period indicators
            period_patterns = [
                r'Q[1-4]\s+20\d{2}',
                r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+20\d{2}',
                r'20\d{2}'
            ]
            
            for pattern in period_patterns:
                match = re.search(pattern, request, re.IGNORECASE)
                if match:
                    period_text = match.group()
                    period_info = self.period_filter.parse_period_request(period_text)
                    break
                    
        except Exception as e:
            print(f"⚠️  Could not parse period from request: {e}")
        
        # Filter datasets by period if specified
        filtered_datasets = {}
        for name, df in datasets.items():
            if period_info:
                filtered_df = self.period_filter.filter_dataframe_by_period(df, period_info)
                filtered_datasets[name] = filtered_df
            else:
                filtered_datasets[name] = df
        
        # Create analysis context
        context = self._build_analysis_context(filtered_datasets, period_info, request)
        
        return context
    
    def _build_analysis_context(self, datasets: Dict[str, pd.DataFrame], period_info: Dict = None, request: str = "") -> str:
        """Build rich context for AI analysis"""
        context_parts = []
        
        # Add request and period information
        context_parts.append(f"USER REQUEST: {request}")
        
        if period_info:
            context_parts.append(f"ANALYSIS PERIOD: {period_info['description']} ({period_info['start_date']} to {period_info['end_date']})")
        
        # Add dataset summaries
        context_parts.append("\nDATASET INFORMATION:")
        
        total_accounts = 0
        total_debits = 0
        total_credits = 0
        
        for name, df in datasets.items():
            if len(df) == 0:
                context_parts.append(f"\n{name}: No data for the specified period")
                continue
                
            accounts = len(df)
            debits = df['debit'].sum() if 'debit' in df.columns else 0
            credits = df['credit'].sum() if 'credit' in df.columns else 0
            
            total_accounts += accounts
            total_debits += debits
            total_credits += credits
            
            context_parts.append(f"""
{name}:
- Accounts: {accounts}
- Total Debits: ${debits:,.2f}
- Total Credits: ${credits:,.2f}
- Balance: ${debits - credits:,.2f}""")
            
            # Add sample transactions
            if accounts > 0:
                sample_accounts = df.head(5)[['account_number', 'account_name', 'debit', 'credit']].to_dict('records')
                context_parts.append(f"- Sample accounts: {sample_accounts}")
        
        # Add summary
        context_parts.append(f"""
OVERALL SUMMARY:
- Total accounts across all datasets: {total_accounts}
- Combined debits: ${total_debits:,.2f}
- Combined credits: ${total_credits:,.2f}
- Net balance: ${total_debits - total_credits:,.2f}
""")
        
        return "\n".join(context_parts)
    
    def run_analysis(self, request: str, file_paths: List[str], file_labels: List[str] = None):
        """Complete analysis pipeline"""
        print("🚀 Starting Dynamic Trial Balance Analysis")
        print("=" * 60)
        
        # Load data
        datasets = self.load_user_data(file_paths, file_labels)
        
        if not datasets:
            print("❌ No datasets loaded successfully")
            return None
        
        # Process request
        context = self.process_user_request(request, datasets)
        
        # Run AI analysis
        result = self._run_ai_analysis(context, request)
        
        # Save results
        self._save_results(result, request, datasets)
        
        return result
    
    def _run_ai_analysis(self, context: str, request: str) -> str:
        """Run AI analysis with CrewAI using DeepSeek API (FIXED)"""
        try:
            # Use the same DeepSeek configuration that works in simple_demo
            from deepseek_config import DeepSeekConfig
            config = DeepSeekConfig.setup_environment()
            print(f"🤖 Using DeepSeek model: {config['model']}")
            
            from crewai import Agent, Task, Crew, Process
            from langchain_openai import ChatOpenAI
            
            # Create LLM instance exactly like working simple_demo
            llm = ChatOpenAI(
                model=config["model"],
                openai_api_base=config["base_url"],
                openai_api_key=config["api_key"],
                temperature=config["temperature"],
                max_tokens=config["max_tokens"]
            )
            
            # Create specialized agent based on request type
            if any(keyword in request.lower() for keyword in ['variance', 'compare', 'change']):
                agent_role = 'Variance Analysis Expert'
                agent_expertise = 'variance analysis, period-over-period comparisons, and identifying material changes'
            elif any(keyword in request.lower() for keyword in ['new', 'added', 'missing']):
                agent_role = 'Account Change Specialist'  
                agent_expertise = 'detecting new accounts, missing transactions, and chart of accounts changes'
            elif any(keyword in request.lower() for keyword in ['tax', 'provision', 'category']):
                agent_role = 'Tax Provision Expert'
                agent_expertise = 'tax categorization, provision calculations, and compliance requirements'
            else:
                agent_role = 'Senior Financial Analyst'
                agent_expertise = 'comprehensive financial analysis, trial balance review, and business insights'
            
            analyst = Agent(
                role=agent_role,
                goal=f'Analyze the financial data and respond to the user request with expert insights',
                backstory=f"""You are a highly experienced {agent_role.lower()} with 15+ years of experience in {agent_expertise}. 
                You provide accurate, actionable insights and identify key risks and opportunities.""",
                verbose=True,
                allow_delegation=False,
                llm=llm  # Pass the working LLM instance
            )
            
            analysis_task = Task(
                description=f"""
                Analyze the provided financial data and respond to this specific user request:
                
                {request}
                
                Data context:
                {context}
                
                Provide a comprehensive response that:
                1. Directly addresses the user's request
                2. Highlights key findings and insights
                3. Identifies any risks or opportunities
                4. Provides actionable recommendations
                5. Notes any data quality issues or limitations
                
                Be specific with numbers and provide clear reasoning for your conclusions.
                """,
                agent=analyst,
                expected_output="A detailed analysis directly addressing the user's request with specific insights, findings, and recommendations"
            )
            
            crew = Crew(
                agents=[analyst],
                tasks=[analysis_task],
                process=Process.sequential,
                verbose=True
            )
            
            print(f"\n🤖 Running AI Analysis with {agent_role} (DeepSeek)...")
            print("-" * 50)
            
            result = crew.kickoff()
            return str(result)
            
        except Exception as e:
            print(f"❌ Error in AI analysis: {e}")
            return f"Analysis failed: {e}"
        
    def _save_results(self, result: str, request: str, datasets: Dict[str, pd.DataFrame]):
        """Save analysis results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        output_data = {
            "analysis_type": "Dynamic User-Driven Analysis",
            "timestamp": timestamp,
            "user_request": request,
            "ai_analysis": result,
            "datasets_summary": {
                name: {
                    "record_count": len(df),
                    "total_debits": float(df['debit'].sum()) if 'debit' in df.columns else 0,
                    "total_credits": float(df['credit'].sum()) if 'credit' in df.columns else 0
                }
                for name, df in datasets.items()
            }
        }
        
        os.makedirs('data/output', exist_ok=True)
        output_file = f"data/output/dynamic_analysis_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\n📁 Results saved to: {output_file}")

def main():
    """Example usage of the dynamic system"""
    print("🎬 Dynamic Trial Balance Analysis System")
    print("=" * 50)
    
    # Check prerequisites
    load_dotenv()
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OpenAI API key not found")
        return
    
    # Initialize system
    system = DynamicTrialBalanceSystem()
    
    # Example usage
    print("\n📝 Example Analysis Requests:")
    print("1. 'Analyze Q1 2024 data for new accounts'")
    print("2. 'Compare variance between Q1 and Q2 2024'") 
    print("3. 'Check for missing expense accounts in March 2024'")
    print("4. 'Categorize all accounts for tax provision'")
    
    # Interactive mode
    while True:
        print("\n" + "="*50)
        request = input("Enter your analysis request (or 'quit' to exit): ").strip()
        
        if request.lower() in ['quit', 'exit', 'q']:
            break
        
        if not request:
            continue
        
        # Get file paths
        print("\nEnter data file paths (comma-separated):")
        file_input = input("Files: ").strip()
        
        if not file_input:
            # Use default demo files
            file_paths = [
                'data/input/trial_balance_2024.csv',
                'data/reference/trial_balance_2023.csv'
            ]
            file_labels = ['Current_Period', 'Prior_Period']
        else:
            file_paths = [f.strip() for f in file_input.split(',')]
            file_labels = [f"Dataset_{i+1}" for i in range(len(file_paths))]
        
        # Run analysis
        try:
            result = system.run_analysis(request, file_paths, file_labels)
            if result:
                print(f"\n🎉 Analysis completed successfully!")
        except Exception as e:
            print(f"❌ Analysis failed: {e}")

if __name__ == "__main__":
    main()