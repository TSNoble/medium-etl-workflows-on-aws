import aws_cdk.core as core
import aws_cdk.aws_s3 as s3


class HelloWorkflowStack(core.Stack):

    def __init__(self, scope, id, *args, **kwargs):
        super().__init__(scope, id, *args, **kwargs)
        source_bucket = s3.Bucket(self, "SourceBucket")
        dest_bucket = s3.Bucket(self, "DestinationBucket")
        processing_bucket = s3.Bucket(self, "ProcessingBucket")
