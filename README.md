### Basic Documentation
###
## 🛠️ Technical Stack
- **Infrastructure**: AWS CDK (Python)
- **ML Pipeline**: SageMaker Pipelines with Processing/Training steps
- **Serving**: SageMaker Endpoint (managed) or Custom Container (FastAPI)

## ✅ Prerequisites
- AWS Account with necessary permissions
- AWS CLI configured
- Docker (for custom inference image)


## 📁 Project Structure
```plaintext
titanic-ml-pipeline/
├── cdk/
│   ├── app.py
│   ├── titanic_stack.py
│   └── requirements.txt
├── processing_scripts/
│   ├── preprocess.py
│   └── requirements.txt
├── training_scripts/
│   ├── train.py
│   └── requirements.txt
├── inference/
│   ├── app.py (FastAPI)
│   ├── lambda_handler.py
│   ├── Dockerfile
│   └── requirements.txt
├── notebooks/
│   └── data_exploration.ipynb
├── pipelines/
│   ├── titanic_pipeline.py
│   └── trigger_pipeline.py
└── README.md
```

next you can find the process to deploy this project to production:



## 📁 Flowchart process
```mermaid
%%{init: {'theme': 'neutral', 'fontFamily': 'Arial', 'gantt': {'barHeight': 20}}}%%
flowchart TD
    A[Start Deployment] --> B[Prerequisites]
    B -->|AWS CLI| C[Configure AWS Credentials]
    B -->|Docker| D[Install Docker]
    B -->|CDK| E[Install AWS CDK]
    C --> F[Clone Repository]
    F --> G[Set Up Python Environment]
    G --> H[Install CDK Dependencies]
    H --> I[Bootstrap CDK]
    I --> J[Deploy Infrastructure]
    J -->|CDK Deploy| K[Create S3 Buckets]
    J -->|CDK Deploy| L[Create IAM Roles]
    J -->|CDK Deploy| M[Create ECR Repository]
    K --> N[Upload Raw Data to S3]
    L --> O[Execute SageMaker Pipeline]
    M --> P[Build & Push Inference Image]
    O -->|Pipeline Runs| Q[Processing Job]
    Q --> R[Training Job]
    R --> S[Model Registration]
    P --> T[Deploy Endpoint]
    S --> T
    T --> U[Test Endpoint]
    U --> V{All Working?}
    V -->|Yes| W[Deployment Complete]
    V -->|No| X[Troubleshoot]
    subgraph AWS Services
        K[S3 Buckets]
        L[IAM Roles]
        M[ECR Repo]
        Q[Data Processing]
        R[Model Training]
        S[Model Registry]
        T[SageMaker Endpoint]
    end
    style A fill:#4CAF50,stroke:#388E3C
    style W fill:#4CAF50,stroke:#388E3C
    style X fill:#F44336,stroke:#D32F2F
    style AWS_Services fill:#E3F2FD,stroke:#64B5F6
```


## 📁 Sequence of operations to do for use this solution
```mermaid
sequenceDiagram
    participant Developer
    participant AWS_CLI
    participant CloudFormation
    participant S3
    participant SageMaker
    participant ECR
    participant ModelRegistry
    participant Endpoint

    %% Deployment Phase
    Developer->>AWS_CLI: 1. cdk bootstrap
    AWS_CLI->>CloudFormation: Initialize CDK toolkit
    Developer->>AWS_CLI: 2. cdk deploy
    AWS_CLI->>CloudFormation: Create/Update Stack
    CloudFormation->>S3: Create buckets (raw/processed)
    CloudFormation->>SageMaker: Setup IAM roles
    CloudFormation->>ECR: Create repository

    %% Data Preparation
    Developer->>AWS_CLI: 3. Upload data (aws s3 cp)
    AWS_CLI->>S3: Store raw dataset

    %% Pipeline Execution
    Developer->>SageMaker: 4. Start Pipeline
    SageMaker->>S3: Read raw data
    SageMaker->>SageMaker: Processing Job
    SageMaker->>S3: Store processed data
    SageMaker->>SageMaker: Training Job
    SageMaker->>ModelRegistry: Register model v1.0

    %% Deployment
    Developer->>AWS_CLI: 5. Build/Push Docker (docker build/push)
    AWS_CLI->>ECR: Store inference image
    Developer->>SageMaker: 6. Deploy endpoint
    SageMaker->>ModelRegistry: Get approved model
    SageMaker->>ECR: Pull inference image
    SageMaker->>Endpoint: Provision resources

    %% Usage Phase
    Endpoint-->>SageMaker: Health check
    Developer->>Endpoint: 7. POST /predict (JSON payload)
    Endpoint->>SageMaker: Execute model
    SageMaker->>Endpoint: Return prediction
    Endpoint->>Developer: Survival probability

    %% Monitoring
    loop CloudWatch
        SageMaker->>CloudWatch: Log metrics
    end

    Note right of Developer: Deployment Complete
```


=======
´´´
>>>>>>> Stashed changes
