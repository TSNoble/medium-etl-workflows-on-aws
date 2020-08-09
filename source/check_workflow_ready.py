from typing import List, Dict

import jmespath
import boto3


def lambda_handler(event, _):
    s3_client = boto3.client("s3")
    s3_files_present = s3_client.list_objects_v2(Bucket=event["InputBucket"])
    return is_workflow_ready(s3_files_present, event["RequiredFiles"])


def is_workflow_ready(s3_files: Dict, required_files: List[str]) -> bool:
    s3_file_keys = jmespath.search("Contents[*].Key", s3_files)
    s3_file_keys = s3_file_keys if s3_file_keys is not None else []
    return is_sublist(required_files, s3_file_keys)


def is_sublist(list1, list2):
    return all(item in list2 for item in list1)
