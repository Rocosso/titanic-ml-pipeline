### Basic Documentation
###
This is the structure of this project
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
