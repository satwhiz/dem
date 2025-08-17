
## Overview
This demo showcases an intelligent multi-agent system built with CrewAI that automates trial balance processing for tax provision preparation. The system demonstrates how specialized AI agents can collaborate to handle complex financial workflows.

## Demo Scenario
- **Entity**: ENT001
- **Current Period**: Q4 2024 
- **Comparison Period**: Q4 2023
- **New Accounts**: 4 new accounts in 2024
- **Material Variances**: Operating expenses +50%, Accounts Receivable +47%

## Agent Team
1. **Data Extractor Agent** - Processes ERP exports
2. **Categorization Agent** - Maps accounts to tax categories
3. **New Account Identifier Agent** - Detects unmapped accounts
4. **Variance Analyzer Agent** - Analyzes period-over-period changes
5. **Compliance Reviewer Agent** - Validates data integrity
6. **Uploader Agent** - Formats output for tax systems

## Quick Start

1. **Setup Environment**
   ```bash
   python -m venv trial-balance-env
   source trial-balance-env/bin/activate  # or Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Configure API Key**
   ```bash
   # Edit .env file
   OPENAI_API_KEY=your_key_here
   ```

3. **Run Demo**
   ```bash
   python run_demo.py
   ```

4. **Optional: Visual Dashboard**
   ```bash
   python run_dashboard.py
   ```

## Expected Results
- ✅ Processes 14 accounts (10 existing + 4 new)
- 🆕 Detects 4 new accounts automatically
- ⚠️ Flags 3 material variances for review
- ✅ Validates trial balance integrity
- 📤 Generates tax provision upload format

## Project Structure
```
trial-balance-demo/
├── data/
│   ├── input/          # Current period data
│   ├── reference/      # Historical data
│   └── output/         # Generated reports
├── src/
│   ├── agents/         # Agent definitions
│   ├── tasks/          # Task definitions
│   ├── tools/          # Custom tools
│   └── config/         # Configuration
└── logs/               # Audit trails
```

## Demo Value Proposition
- **85% automation** of manual trial balance processing
- **Hours vs Days** for multi-entity close cycles
- **Audit-grade traceability** with decision reasoning
- **Intelligent error handling** and validation
- **Seamless integration** with existing systems