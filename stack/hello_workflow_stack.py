from pathlib import Path

import aws_cdk.core as core
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_lambda as aws_lambda


SOURCE_PATH = Path(__file__).parent.parent.joinpath("source")

class HelloWorkflowStack(core.Stack):

    def __init__(self, scope, id, *args, **kwargs):
        super().__init__(scope, id, *args, **kwargs)

        # Buckets
        source_bucket = s3.Bucket(self, "SourceBucket")
        dest_bucket = s3.Bucket(self, "DestinationBucket")
        processing_bucket = s3.Bucket(self, "ProcessingBucket")

        # Lambda Functions
        check_workflow_ready_lambda = aws_lambda.Function(
            self, "CheckWorkflowReady",
            code=aws_lambda.Code.from_asset(SOURCE_PATH/"check_workflow_ready"),
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler="lambda_handler"
        )

        # State Machine
