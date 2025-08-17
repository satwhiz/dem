from crewai import Task

class TrialBalanceTasks:
    
    def data_extraction_task(self, agent, trial_balance_file):
        return Task(
            description=f"""
            Extract and validate trial balance data from the file: {trial_balance_file}
            
            Your tasks:
            1. Load the trial balance data from the specified file
            2. Validate data completeness (check for required columns)
            3. Verify data quality (check for missing values, duplicates)
            4. Calculate basic totals (total debits, credits, balance)
            5. Provide a summary of the extracted data
            
            Requirements:
            - Ensure all required columns are present
            - Flag any data quality issues
            - Provide account count and balance totals
            """,
            agent=agent,
            expected_output="A detailed summary of extracted trial balance data with validation results and basic statistics"
        )
    
    def categorization_task(self, agent, accounts_to_categorize):
        return Task(
            description=f"""
            Categorize the following accounts for tax reporting purposes:
            {accounts_to_categorize}
            
            Your tasks:
            1. Review each account number and name
            2. Apply categorization rules based on account ranges
            3. Assign appropriate tax categories
            4. Provide confidence scores for each categorization
            5. Flag any accounts that need manual review
            
            Requirements:
            - Use standard accounting categorization (Asset, Liability, Equity, Revenue, Expense)
            - Assign tax-specific subcategories where applicable
            - Provide reasoning for each categorization decision
            """,
            agent=agent,
            expected_output="A complete list of categorized accounts with categories, tax classifications, confidence scores, and reasoning"
        )
    
    def new_account_identification_task(self, agent, current_file, prior_file):
        return Task(
            description=f"""
            Compare current period ({current_file}) with prior period ({prior_file}) 
            to identify new accounts that require categorization.
            
            Your tasks:
            1. Perform variance analysis between the two periods
            2. Identify accounts present in current but not in prior period
            3. For each new account, determine appropriate categorization
            4. Assess the business impact of new accounts
            5. Flag accounts requiring special attention
            
            Requirements:
            - Provide list of all new accounts with details
            - Categorize new accounts using the categorization agent
            - Assess materiality of new accounts
            """,
            agent=agent,
            expected_output="A comprehensive report of new accounts with their categorizations and business impact assessment"
        )
    
    def variance_analysis_task(self, agent, current_file, prior_file):
        return Task(
            description=f"""
            Perform detailed variance analysis between current period ({current_file}) 
            and prior period ({prior_file}).
            
            Your tasks:
            1. Compare account balances between periods
            2. Calculate variance amounts and percentages
            3. Identify material variances (>15% threshold)
            4. Provide potential explanations for significant variances
            5. Summarize overall trends and patterns
            
            Requirements:
            - Flag all variances exceeding materiality threshold
            - Provide variance analysis in both absolute and percentage terms
            - Highlight accounts requiring further investigation
            """,
            agent=agent,
            expected_output="A detailed variance analysis report with material variances highlighted and potential explanations"
        )
    
    def compliance_review_task(self, agent, processed_data):
        return Task(
            description=f"""
            Perform final compliance and quality review of processed trial balance data.
            
            Your tasks:
            1. Verify trial balance equation (Debits = Credits)
            2. Ensure all accounts are properly categorized
            3. Check for completeness of required fields
            4. Validate data integrity and consistency
            5. Confirm compliance with accounting standards
            
            Requirements:
            - Trial balance must be in balance (difference < $0.01)
            - All accounts must have assigned categories
            - No missing or invalid data
            - Generate compliance attestation
            """,
            agent=agent,
            expected_output="A compliance report confirming data quality and regulatory requirements are met, with any issues flagged for resolution"
        )
    
    def upload_preparation_task(self, agent, validated_data):
        return Task(
            description=f"""
            Prepare validated trial balance data for upload to tax provision systems.
            
            Your tasks:
            1. Format data according to tax provision system requirements
            2. Create upload file in required format (JSON/XML/CSV)
            3. Generate upload manifest and documentation
            4. Perform pre-upload validation checks
            5. Create audit trail for the upload process
            
            Requirements:
            - Output must be in standard tax provision format
            - Include all required metadata
            - Generate upload confirmation and audit trail
            """,
            agent=agent,
            expected_output="A properly formatted tax provision upload file with documentation and audit trail"
        )