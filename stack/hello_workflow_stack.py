from pathlib import Path

import aws_cdk.core as core
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_lambda as aws_lambda
import aws_cdk.aws_stepfunctions as sf
import aws_cdk.aws_stepfunctions_tasks as sf_tasks


DIST_PATH = Path(__file__).parent.parent.joinpath("dist").absolute()


class HelloWorkflowStack(core.Stack):

    def __init__(self, scope, id, *args, **kwargs):
        super().__init__(scope, id, *args, **kwargs)

        # Buckets
        source_bucket = s3.Bucket(self, "SourceBucket")
        dest_bucket = s3.Bucket(self, "DestinationBucket")
        processing_bucket = s3.Bucket(self, "ProcessingBucket")

        # Lambda Functions
        generate_workflow_input_lambda = aws_lambda.Function(
            self, "GenerateWorkflowInputFunction",
            code=aws_lambda.Code.from_asset(str(DIST_PATH)),
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler="generate_workflow_input.lambda_handler"
        )
        check_workflow_ready_lambda = aws_lambda.Function(
            self, "CheckWorkflowReadyFunction",
            code=aws_lambda.Code.from_asset(str(DIST_PATH)),
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler="check_workflow_ready.lambda_handler"
        )
        string_replace_lambda = aws_lambda.Function(
            self, "StringReplaceFunction",
            code=aws_lambda.Code.from_asset(str(DIST_PATH)),
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler="string_replace.lambda_handler"
        )
        calculate_total_earnings_lambda = aws_lambda.Function(
            self, "CalculateTotalEarningsFunction",
            code=aws_lambda.Code.from_asset(str(DIST_PATH)),
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler="calculate_total_earnings.lambda_handler"
        )
        convert_csv_to_json_lambda = aws_lambda.Function(
            self, "ConvertCsvToJsonFunction",
            code=aws_lambda.Code.from_asset(str(DIST_PATH)),
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler="convert_csv_to_json.lambda_handler"
        )

        # Permissions
        source_bucket.grant_read(check_workflow_ready_lambda)
        source_bucket.grant_read(string_replace_lambda)
        processing_bucket.grant_write(string_replace_lambda)
        processing_bucket.grant_read_write(calculate_total_earnings_lambda)
        processing_bucket.grant_read(convert_csv_to_json_lambda)
        dest_bucket.grant_write(convert_csv_to_json_lambda)

        # Outputs
        core.CfnOutput(self, "SourceBucketName", value=source_bucket.bucket_name)
        core.CfnOutput(self, "DestinationBucketName", value=dest_bucket.bucket_name)
        core.CfnOutput(self, "ProcessingBucketName", value=processing_bucket.bucket_name)
        core.CfnOutput(self, "GenerateWorkflowInputLambda", value=generate_workflow_input_lambda.function_name)
        core.CfnOutput(self, "CheckWorkflowReadyLambda", value=check_workflow_ready_lambda.function_name)
        core.CfnOutput(self, "StringReplaceLambda", value=string_replace_lambda.function_name)
        core.CfnOutput(self, "CalculateTotalEarningsLambda", value=calculate_total_earnings_lambda.function_name)
        core.CfnOutput(self, "ConvertCsvToJsonLambda", value=convert_csv_to_json_lambda.function_name)

        # State Machine
        generate_workflow_input_task = sf_tasks.LambdaInvoke(
            self, "GenerateWorkflowInput",
            lambda_function=generate_workflow_input_lambda,
            payload_response_only=True
        )
        check_workflow_ready_task = sf_tasks.LambdaInvoke(
            self, "CheckWorkflowReady",
            lambda_function=check_workflow_ready_lambda,
            input_path="$.CheckWorkflowReady.Input",
            result_path="$.CheckWorkflowReady.Output",
            payload_response_only=True
        )
        string_replace_task = sf_tasks.LambdaInvoke(
            self, "ReplaceString",
            lambda_function=string_replace_lambda,
            input_path="$.StringReplace.Input",
            output_path="$.Payload",
            result_path="$.StringReplace.Output",
            payload_response_only=True
        )
        calculate_total_earnings_task = sf_tasks.LambdaInvoke(
            self, "CalculateTotalEarnings",
            lambda_function=calculate_total_earnings_lambda,
            input_path="$.CalculateTotalEarnings.Input",
            output_path="$.Payload",
            result_path="$.CalculateTotalEarnings.Output",
            payload_response_only=True
        )
        convert_csv_to_json_task = sf_tasks.LambdaInvoke(
            self, "ConvertCsvToJson",
            lambda_function=convert_csv_to_json_lambda,
            input_path="$.ConvertCsvToJson.Input",
            output_path="$.Payload",
            result_path="$.ConvertCsvToJson.Output",
            payload_response_only=True
        )

        end_task = sf.Succeed(self, "WorkflowEnd")

        workflow_steps = sf.Chain.\
            start(string_replace_task)\
            .next(calculate_total_earnings_task)\
            .next(convert_csv_to_json_task)\
            .next(end_task)

        run_workflow = sf.Choice(self, "RunWorkflowDecision")\
            .when(sf.Condition.boolean_equals("$.CheckWorkflowReady.Output", True), workflow_steps)\
            .otherwise(end_task)

        hello_workflow_state_machine = sf.StateMachine(
            self, "HelloWorkflowStateMachine",
            definition=sf.Chain\
                .start(check_workflow_ready_task)\
                .next(run_workflow)
        )
