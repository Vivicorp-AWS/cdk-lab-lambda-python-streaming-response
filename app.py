#!/usr/bin/env python3
import os

import aws_cdk as cdk
from stacks.lambda_stack import LambdaLayerStack

app = cdk.App()
env = cdk.Environment(
    region="ap-northeast-1",
    )

lambdalayer_stack = LambdaLayerStack(
    app, "cdklab-lambdastreaming-stack",
    description="CDK Lab for Lambda with Streaming Feature",
    env=env,
    region=env.region,
    )

app.synth()
