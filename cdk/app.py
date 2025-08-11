#!/usr/bin/env python3
import os
from aws_cdk import App
from titanic_stack import TitanicMlStack

app = App()

# Contextos configurables (pueden pasarse via -c flag)
env = {
    "account": os.getenv("CDK_DEFAULT_ACCOUNT"),
    "region": os.getenv("CDK_DEFAULT_REGION")
}

TitanicMlStack(
    app, "TitanicMlStack",
    description="Stack para el pipeline de ML del dataset Titanic",
    env=env
)

app.synth()
