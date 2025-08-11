import os
import boto3
import sagemaker
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep
from sagemaker.workflow.model_step import ModelStep
from sagemaker.processing import ScriptProcessor
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.model import Model
from sagemaker.inputs import TrainingInput
from sagemaker.workflow.parameters import ParameterString

def get_pipeline(
    region,
    role,
    default_bucket,
    pipeline_name,
    processing_instance_count,
    training_instance_count,
    model_approval_status
):
    # Parámetros del pipeline
    input_data = ParameterString(
        name="InputData",
        default_value=f"s3://{default_bucket}/raw/titanic.csv"
    )

    # Paso de procesamiento
    script_processor = ScriptProcessor(
        image_uri=sagemaker.image_uris.retrieve("framework", region, "latest", "scikit-learn"),
        command=["python3"],
        instance_type="ml.m5.xlarge",
        instance_count=processing_instance_count,
        base_job_name="titanic-preprocessing",
        role=role
    )

    processing_step = ProcessingStep(
        name="PreprocessTitanicData",
        processor=script_processor,
        inputs=[sagemaker.processing.ProcessingInput(
            source=input_data,
            destination="/opt/ml/processing/input"
        )],
        outputs=[
            sagemaker.processing.ProcessingOutput(
                output_name="train",
                source="/opt/ml/processing/train",
                destination=f"s3://{default_bucket}/processed/train"
            ),
            sagemaker.processing.ProcessingOutput(
                output_name="test",
                source="/opt/ml/processing/test",
                destination=f"s3://{default_bucket}/processed/test"
            )
        ],
        code="processing_scripts/preprocess.py"
    )

    # Paso de entrenamiento
    sklearn_estimator = SKLearn(
        entry_point="train.py",
        source_dir="training_scripts",
        instance_type="ml.m5.xlarge",
        instance_count=training_instance_count,
        framework_version="1.0-1",
        role=role,
        hyperparameters={
            "n-estimators": 100,
            "min-samples-leaf": 3,
            "random-state": 42
        }
    )

    training_step = TrainingStep(
        name="TrainTitanicModel",
        estimator=sklearn_estimator,
        inputs={
            "train": TrainingInput(
                s3_data=processing_step.properties.ProcessingOutputConfig.Outputs["train"].S3Output.S3Uri,
                content_type="text/csv"
            ),
            "test": TrainingInput(
                s3_data=processing_step.properties.ProcessingOutputConfig.Outputs["test"].S3Output.S3Uri,
                content_type="text/csv"
            )
        }
    )

    # Paso de registro del modelo
    model = Model(
        image_uri=sklearn_estimator.training_image_uri(),
        model_data=training_step.properties.ModelArtifacts.S3ModelArtifacts,
        entry_point="train.py",
        source_dir="training_scripts",
        sagemaker_session=sagemaker_session,
        role=role
    )

    model_step = ModelStep(
        name="RegisterTitanicModel",
        step_args=model.register(
            content_types=["text/csv"],
            response_types=["text/csv"],
            inference_instances=["ml.t2.medium", "ml.m5.xlarge"],
            transform_instances=["ml.m5.xlarge"],
            model_package_group_name="TitanicSurvival",
            approval_status=model_approval_status
        )
    )

    # Creación del pipeline
    pipeline = Pipeline(
        name=pipeline_name,
        parameters=[
            input_data,
            processing_instance_count,
            training_instance_count,
            model_approval_status
        ],
        steps=[processing_step, training_step, model_step]
    )

    return pipeline
