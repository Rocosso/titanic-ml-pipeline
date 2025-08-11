from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
    aws_sagemaker as sagemaker,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    RemovalPolicy,
    aws_ecr as ecr,
    CfnOutput
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

        # Crear repositorio ECR para la imagen de inferencia
        ecr_repo = ecr.Repository(
            self, "InferenceRepo",
            repository_name="titanic-inference",
            image_scan_on_push=True,
            removal_policy=RemovalPolicy.DESTROY
        )

        # Rol para el endpoint
        endpoint_role = iam.Role(
            self, "EndpointRole",
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchLogsFullAccess")
            ]
        )

        # Configuración del endpoint
        endpoint_config = sagemaker.CfnEndpointConfig(
            self, "TitanicEndpointConfig",
            production_variants=[{
                "initial_instance_count": 1,
                "instance_type": "ml.m5.large",
                "model_name": "TitanicSurvivalModel",
                "variant_name": "AllTraffic",
                "initial_variant_weight": 1
            }],
            async_inference_config={
                "client_config": {
                    "max_concurrent_invocations_per_instance": 4
                },
                "output_config": {
                    "s3_output_path": f"s3://{self.processed_data_bucket.bucket_name}/inference_outputs"
                }
            }
        )

        # Endpoint de SageMaker
        endpoint = sagemaker.CfnEndpoint(
            self, "TitanicEndpoint",
            endpoint_config_name=endpoint_config.attr_endpoint_config_name,
            endpoint_name="TitanicSurvivalEndpoint"
        )

        # Outputs útiles
        CfnOutput(self, "EndpointName", value=endpoint.endpoint_name)
        CfnOutput(self, "ECRRepoURI", value=ecr_repo.repository_uri)
