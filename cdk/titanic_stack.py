from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
    aws_sagemaker as sagemaker,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    RemovalPolicy
)
from constructs import Construct

class TitanicMlStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Creación de buckets S3
        self.raw_data_bucket = s3.Bucket(
            self, "TitanicRawData",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED
        )

        self.processed_data_bucket = s3.Bucket(
            self, "TitanicProcessedData",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED
        )

        # Rol IAM para SageMaker
        self.sagemaker_role = iam.Role(
            self, "SageMakerExecutionRole",
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchLogsFullAccess")
            ]
        )

        # Lambda para la API de inferencia
        inference_lambda = _lambda.Function(
            self, "InferenceLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("inference"),
            handler="lambda_handler.handler",
            environment={
                "MODEL_NAME": "titanic-survival-predictor"
            }
        )

        # API Gateway
        api = apigw.LambdaRestApi(
            self, "TitanicApi",
            handler=inference_lambda,
            proxy=False
        )

        predict_resource = api.root.add_resource("predict")
        predict_resource.add_method("POST")
