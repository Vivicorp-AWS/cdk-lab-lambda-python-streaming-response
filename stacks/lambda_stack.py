import aws_cdk as cdk
from aws_cdk import (
    aws_lambda as lambda_,
    RemovalPolicy,
    Stack,
    aws_logs as logs,
    CfnOutput,
)
from constructs import Construct
from cdk_lambda_layer_builder.constructs import BuildPyLayerAsset


class LambdaLayerStack(Stack):
    def __init__(self, scope: Construct, id: str, region: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        print("=====REGION=====")
        print(region)

        # Create layer includes FastAPI and uvicorn
        pkgs_layer_asset = BuildPyLayerAsset.from_pypi(self, 'PyPiLayerAsset',
            pypi_requirements=['fastapi', 'uvicorn'],
            py_runtime=lambda_.Runtime.PYTHON_3_12,
        )
        pkgs_layer = lambda_.LayerVersion(
            self, 'py13-fastapi-uvicorn-layer',
            description='Lambda Layer includes FastAPI and uvicorn',
            code=lambda_.Code.from_bucket(pkgs_layer_asset.asset_bucket, pkgs_layer_asset.asset_key),
            compatible_architectures=[lambda_.Architecture.ARM_64],
            compatible_runtimes=[
                lambda_.Runtime.PYTHON_3_12,
                ],
            removal_policy=RemovalPolicy.DESTROY,
            )

        # create lambda function
        function = lambda_.Function(
            self, "lambda_function",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="run.sh",
            code=lambda_.Code.from_asset("lambda_code"),
            environment={
                "AWS_LAMBDA_EXEC_WRAPPER": "/opt/bootstrap",
                "AWS_LWA_INVOKE_MODE": "response_stream",
                "PORT": "8000",
                },
            architecture=lambda_.Architecture.ARM_64,
            layers=[
                lambda_.LayerVersion.from_layer_version_arn(  # AWS Lambda Web Adapter layer
                    self, "AWSLambdaWebAdapterLayer",
                    layer_version_arn=f"arn:aws:lambda:{region}:753240598075:layer:LambdaAdapterLayerArm64:24",
                ),
                lambda_.LayerVersion.from_layer_version_arn(  # # Klayer's Boto3 layer
                    self, "KlayersBoto3Layer",
                    layer_version_arn=f"arn:aws:lambda:{region}:770693421928:layer:Klayers-p312-arm64-boto3:24",
                ),
                pkgs_layer,
                ],
            log_group=logs.LogGroup(
                self, "lambda-log-group",
                removal_policy=RemovalPolicy.DESTROY,
                retention=logs.RetentionDays.ONE_MONTH,
                ),
            timeout=cdk.Duration.seconds(60),
            )
        
        # Add "AmazonBedrockLimitedAccess" managed policy to lambda execution role
        function.role.add_managed_policy(
            cdk.aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonBedrockLimitedAccess")
            )

        function_url = function.add_function_url(
            auth_type=lambda_.FunctionUrlAuthType.NONE,
            invoke_mode=lambda_.InvokeMode.RESPONSE_STREAM,
        )

        CfnOutput(
            self,
            "FunctionURL",
            value=function_url.url,
        )
