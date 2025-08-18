```mermaid
graph TB
    %% User Input Layer
    User[User Request<br/>Analyze Q1 2024 for new accounts]
    
    %% Data Sources
    subgraph DataSources["Data Sources"]
        SAP[SAP Export<br/>gl_account, dr_amount<br/>cr_amount, period_ending]
        Oracle[Oracle Export<br/>account_id, debit<br/>credit, as_of_date]
        Excel[Excel Export<br/>Account Number<br/>Debit Amount, Credit Amount]
    end
    
    %% System Entry Point
    DynamicSystem[Dynamic Trial Balance System<br/>Entry Point]
    
    %% Schema Detection & Standardization
    subgraph SchemaProcessing["Schema Processing"]
        SchemaDetector[DataSchemaMapper<br/>Auto-detect column formats]
        Standardizer[Standardize to Common Schema<br/>account_number, account_name<br/>debit, credit, period]
    end
    
    %% Period Intelligence
    subgraph PeriodProcessing["Period Intelligence"]
        PeriodParser[Parse Request<br/>Q1 2024 to Jan-Mar 2024]
        PeriodFilter[Filter Data by Period<br/>74 records to 39 Q1 records]
    end
    
    %% Agent Selection Logic
    AgentSelector{Agent Selection Logic<br/>Based on Keywords}
    
    %% The Six AI Agents
    subgraph AIAgents["Specialized AI Agents"]
        DataExtractor[Data Extractor Agent<br/>Role: Data Specialist<br/>Tools: load_trial_balance]
        Categorizer[Categorization Agent<br/>Role: Tax Expert<br/>Tools: categorize_account]
        NewAccountAgent[New Account Agent<br/>Role: Change Specialist<br/>Tools: variance_analysis]
        VarianceAgent[Variance Analyzer<br/>Role: Financial Analyst<br/>Tools: variance_analysis]
        ComplianceAgent[Compliance Reviewer<br/>Role: Quality Assurance<br/>Tools: validate_compliance]
        UploaderAgent[Uploader Agent<br/>Role: Integration Specialist<br/>Tools: prepare_upload_format]
    end
    
    %% AI Tools
    subgraph Tools["AI-Powered Tools"]
        LoadTB[load_trial_balance<br/>Validates data quality<br/>Calculates totals]
        CategorizeAcc[categorize_account<br/>Maps to Asset/Liability<br/>Assigns tax categories]
        VarianceAnalysis[variance_analysis<br/>Compares periods<br/>Flags material changes]
        ValidateComp[validate_compliance<br/>Checks trial balance<br/>Validates completeness]
        PrepareUpload[prepare_upload_format<br/>Creates tax provision<br/>upload files]
    end
    
    %% AI Processing Engine
    subgraph AIEngine["AI Processing Engine"]
        DeepSeek[DeepSeek AI Model<br/>Natural Language Understanding<br/>Financial Expertise]
        CrewAI[CrewAI Framework<br/>Multi-Agent Orchestration<br/>Task Coordination]
    end
    
    %% Analysis Results
    subgraph AnalysisResults["Analysis Results"]
        NewAccounts[New Accounts Found<br/>Account 1600: Finished Goods 25K<br/>Account 2200: Customer Advances 15K<br/>Account 5400: IT Infrastructure 8K]
        Categories[Account Categories<br/>1600 to Asset Inventory<br/>2200 to Liability Deferred Revenue<br/>5400 to Expense Deductible]
        BusinessInsights[Business Insights<br/>New product line indication<br/>Strong customer pre-orders<br/>Technology investment<br/>Risk assessments]
        Recommendations[Recommendations<br/>Establish inventory controls<br/>Create revenue recognition policy<br/>Track IT investment ROI<br/>Monitor compliance]
    end
    
    %% Output Generation
    subgraph OutputGeneration["Output Generation"]
        AnalysisReport[Analysis Report<br/>Professional insights<br/>Business explanations<br/>Risk assessments]
        TaxUpload[Tax Provision Upload<br/>Categorized accounts<br/>Deferred tax implications<br/>Compliance validation]
        AuditTrail[Audit Trail<br/>Decision reasoning<br/>Agent actions log<br/>Data lineage]
        Dashboard[Dashboard/Visual<br/>Charts and graphs<br/>Key metrics<br/>Trend analysis]
    end
    
    %% Data Flow Connections
    User --> DynamicSystem
    DataSources --> SchemaDetector
    DynamicSystem --> SchemaDetector
    SchemaDetector --> Standardizer
    User --> PeriodParser
    PeriodParser --> PeriodFilter
    Standardizer --> PeriodFilter
    
    PeriodFilter --> AgentSelector
    
    %% Agent Selection Paths
    AgentSelector -->|"new accounts"| NewAccountAgent
    AgentSelector -->|"variance"| VarianceAgent
    AgentSelector -->|"categorize"| Categorizer
    AgentSelector -->|"compliance"| ComplianceAgent
    
    %% Agent Tool Usage
    DataExtractor --> LoadTB
    Categorizer --> CategorizeAcc
    NewAccountAgent --> VarianceAnalysis
    NewAccountAgent --> CategorizeAcc
    VarianceAgent --> VarianceAnalysis
    ComplianceAgent --> ValidateComp
    UploaderAgent --> PrepareUpload
    
    %% AI Engine Connections
    AIAgents --> CrewAI
    CrewAI --> DeepSeek
    Tools --> DeepSeek
    
    %% Results Generation
    DeepSeek --> NewAccounts
    DeepSeek --> Categories
    DeepSeek --> BusinessInsights
    DeepSeek --> Recommendations
    
    %% Output Generation
    AnalysisResults --> AnalysisReport
    AnalysisResults --> TaxUpload
    AnalysisResults --> AuditTrail
    AnalysisResults --> Dashboard
    
    %% Example Data Flow Labels
    User -.->|Example: Q1 2024 new accounts| DynamicSystem
    SAP -.->|74 records with<br/>SAP schema| SchemaDetector
    SchemaDetector -.->|Auto-detected<br/>mapping rules| Standardizer
    Standardizer -.->|Standardized<br/>74 records| PeriodFilter
    PeriodFilter -.->|Filtered to<br/>39 Q1 records| AgentSelector
    NewAccountAgent -.->|Found 3 new<br/>accounts| NewAccounts
    Categories -.->|Asset, Liability<br/>Expense categories| BusinessInsights
    
    %% Styling
    classDef userInput fill:#e1f5fe
    classDef dataSource fill:#f3e5f5
    classDef processing fill:#e8f5e8
    classDef agent fill:#fff3e0
    classDef tool fill:#fce4ec
    classDef ai fill:#e3f2fd
    classDef result fill:#f1f8e9
    classDef output fill:#fafafa
    
    class User userInput
    class SAP,Oracle,Excel dataSource
    class SchemaDetector,Standardizer,PeriodParser,PeriodFilter processing
    class DataExtractor,Categorizer,NewAccountAgent,VarianceAgent,ComplianceAgent,UploaderAgent agent
    class LoadTB,CategorizeAcc,VarianceAnalysis,ValidateComp,PrepareUpload tool
    class DeepSeek,CrewAI ai
    class NewAccounts,Categories,BusinessInsights,Recommendations result
    class AnalysisReport,TaxUpload,AuditTrail,Dashboard output

    ```ß