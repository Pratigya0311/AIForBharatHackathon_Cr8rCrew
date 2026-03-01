#!/usr/bin/env python3
"""
CDK App entry point for TrendScribe infrastructure deployment.
Instantiates and deploys the TrendScribe stack to AWS.

Deployment:
  cdk deploy

Destroy:
  cdk destroy
"""

from aws_cdk import App, Environment
from cdk_stack import TrendScribeStack

app = App()

TrendScribeStack(
    app,
    "TrendScribeStack",
    env=Environment(
        account=None,  # Uses AWS_ACCOUNT_ID from environment or CLI
        region=None,   # Uses AWS_REGION from environment or CLI
    ),
)

app.synth()
