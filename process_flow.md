```mermaid
flowchart TD
    %% Input Phase
    A[User Input<br/>Analyze Q1 2024 for new accounts]
    
    %% Data Loading Phase
    B[Load Data Files<br/>SAP: sap_full_year_2024.csv<br/>Oracle: oracle_q2_2024.csv<br/>Excel: excel_export_2023.csv]
    
    %% Schema Detection
    C[Auto-Detect Schema<br/>SAP: gl_account to account_number<br/>Oracle: account_id to account_number<br/>Excel: Account Number to account_number]
    
    %% Period Parsing
    D[Parse Period Request<br/>Q1 2024 to Jan 1 to Mar 31, 2024]
    
    %% Data Filtering
    E[Filter Data by Period<br/>Original: 74 records<br/>Filtered: 39 Q1 records<br/>Total Debits: 1,802,500<br/>Total Credits: 1,515,000]
    
    %% Agent Selection
    F{Select Appropriate Agent<br/>Keywords: new, accounts<br/>Account Change Specialist}
    
    %% Agent Execution
    G[Account Change Specialist<br/>Analyzes Q1 data for new accounts<br/>Uses: variance_analysis tool<br/>Uses: categorize_account tool]
    
    %% Tool Execution Phase
    subgraph ToolExecution["Tool Execution"]
        H1[variance_analysis<br/>Compares Jan vs Mar accounts<br/>Jan: 1000,1100,1150,1500,2000<br/>Mar: 1000,1100,1150,1500,1600,2000,2200<br/>New: 1600,2200,5400]
        
        H2[categorize_account 1600<br/>Account: Finished Goods<br/>Range: 1000-1999 = Asset<br/>Tax Category: Current Asset<br/>Confidence: 95%]
        
        H3[categorize_account 2200<br/>Account: Customer Advances<br/>Range: 2000-2999 = Liability<br/>Tax Category: Current Liability<br/>Confidence: 95%]
        
        H4[categorize_account 5400<br/>Account: IT Infrastructure<br/>Range: 5000-5999 = Expense<br/>Tax Category: Deductible Expense<br/>Confidence: 95%]
    end
    
    %% AI Processing
    I[DeepSeek AI Processing<br/>CrewAI Task Execution<br/>Natural Language Analysis<br/>Business Insight Generation]
    
    %% Results Generation
    J[Generate Analysis Results<br/>3 New Accounts Identified<br/>Categories Assigned<br/>Business Insights Generated<br/>Recommendations Provided]
    
    %% Output Phase
    subgraph OutputPhase["Output Generation"]
        K1[Analysis Report<br/>Professional insights<br/>Risk assessments<br/>Action recommendations]
        
        K2[JSON Output<br/>Structured data<br/>Audit trail<br/>Timestamp: 20250818_033650]
        
        K3[Dashboard Display<br/>Visual charts<br/>Key metrics<br/>Trend analysis]
        
        K4[Tax Upload Format<br/>Categorized accounts<br/>Deferred tax implications<br/>Compliance validation]
    end
    
    %% Error Handling
    L{Error Handling<br/>Data Quality Issues?<br/>Missing Files?<br/>API Failures?}
    
    M[Error Resolution<br/>Retry mechanisms<br/>Fallback procedures<br/>User notifications]
    
    %% Flow Connections
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H1
    G --> H2
    G --> H3
    G --> H4
    H1 --> I
    H2 --> I
    H3 --> I
    H4 --> I
    I --> J
    J --> K1
    J --> K2
    J --> K3
    J --> K4
    
    %% Error Flow
    B --> L
    C --> L
    E --> L
    G --> L
    I --> L
    L -->|Yes| M
    L -->|No| J
    M --> G
    
    %% Detailed Annotations
    A -.->|Example Input| B
    B -.->|Multiple formats handled automatically| C
    C -.->|Schema mapped to standard format| D
    D -.->|Smart period understanding| E
    E -.->|Data subset for analysis| F
    F -.->|AI agent selection| G
    G -.->|Specialized analysis tools| ToolExecution
    I -.->|AI-powered insights| J
    J -.->|Multiple output formats| OutputPhase
    
    %% Styling
    classDef input fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef processing fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef agent fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    classDef tool fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef ai fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef output fill:#f1f8e9,stroke:#388e3c,stroke-width:2px
    classDef error fill:#ffebee,stroke:#d32f2f,stroke-width:2px
    
    class A input
    class B,C,D,E processing
    class F,G agent
    class H1,H2,H3,H4 tool
    class I ai
    class J,K1,K2,K3,K4 output
    class L,M error
    ```