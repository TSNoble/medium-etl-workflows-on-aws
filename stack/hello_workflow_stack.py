from pathlib import Path

import aws_cdk.core as core
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_lambda as aws_lambda


DIST_PATH = Path(__file__).parent.parent.joinpath("dist").absolute()


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
            code=aws_lambda.Code.from_asset(str(DIST_PATH)),
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler="check_workflow_ready.lambda_handler"
        )
        string_replace_lambda = aws_lambda.Function(
            self, "StringReplace",
            code=aws_lambda.Code.from_asset(str(DIST_PATH)),
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler="string_replace.lambda_handler"
        )
        convert_csv_to_json_lambda = aws_lambda.Function(
            self, "ConvertCsvToJson",
            code=aws_lambda.Code.from_asset(str(DIST_PATH)),
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler="convert_csv_to_json.lambda_handler"
        )

        # Permissions
        source_bucket.grant_read(check_workflow_ready_lambda)
        source_bucket.grant_read(string_replace_lambda)
        processing_bucket.grant_write(string_replace_lambda)
        processing_bucket.grant_read(convert_csv_to_json_lambda)
        dest_bucket.grant_write(convert_csv_to_json_lambda)

        # Outputs
        core.CfnOutput(self, "SourceBucketName", value=source_bucket.bucket_name)
        core.CfnOutput(self, "DestinationBucketName", value=dest_bucket.bucket_name)
        core.CfnOutput(self, "ProcessingBucketName", value=processing_bucket.bucket_name)
        core.CfnOutput(self, "CheckWorkflowReadyLambda", value=check_workflow_ready_lambda.function_name)
        core.CfnOutput(self, "StringReplaceLambda", value=string_replace_lambda.function_name)
        core.CfnOutput(self, "ConvertCsvToJsonLambda", value=convert_csv_to_json_lambda.function_name)

        # State Machine
