import json
import boto3
import os

runtime = boto3.client("runtime.sagemaker")
model_name = os.environ["MODEL_NAME"]

def handler(event, context):
    try:
        # Parsear datos de entrada
        body = json.loads(event["body"])

        # Convertir a CSV para el modelo
        input_data = ",".join([
            str(body["Pclass"]),
            str(body["Sex"]),
            str(body["Age"]),
            str(body["SibSp"]),
            str(body["Parch"]),
            str(body["Fare"]),
            str(body["Embarked"])
        ])

        # Invocar endpoint
        response = runtime.invoke_endpoint(
            EndpointName=f"{model_name}-endpoint",
            ContentType="text/csv",
            Body=input_data
        )

        result = json.loads(response["Body"].read().decode())

        return {
            "statusCode": 200,
            "body": json.dumps({
                "survived": bool(result["predictions"][0]),
                "probability": result["predictions"][1]
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
