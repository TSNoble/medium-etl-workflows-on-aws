import os


def lambda_handler(_, __):
    input_bucket_name = os.environ["InputBucketName"]
    processing_bucket_name = os.environ["ProcessingBucketName"]
    output_bucket_name = os.environ["OutputBucketName"]
    check_workflow_ready_input = {
        "InputBucket": input_bucket_name,
        "RequiredFiles": ["people.csv", "jobs.csv"]
    }
    string_replace_common_input = {
        "InputBucket": input_bucket_name,
        "ToReplace": "Programming",
        "ReplaceWith": "Coding",
        "OutputBucket": processing_bucket_name
    }
    string_replace_input = [
        {**string_replace_common_input, "InputKey": "people.csv", "OutputKey": "string_replace/people.csv"},
        {**string_replace_common_input, "InputKey": "jobs.csv", "OutputKey": "string_replace/jobs.csv"}
    ]
    calculate_total_earnings_input = {
        "InputBucket": processing_bucket_name,
        "PeopleKey": "string_replace/people.csv",
        "JobsKey": "string_replace/jobs.csv",
        "OutputBucket": processing_bucket_name,
        "OutputKey": "calculate_total_earnings/merged.csv"
    }
    convert_csv_to_json_input = {
        "InputBucket": processing_bucket_name,
        "InputKey": "calculate_total_earnings/merged.csv",
        "OutputBucket": output_bucket_name,
        "OutputKey": "output.json"
    }
    workflow_input = {
        "CheckWorkflowReady": {"Input": check_workflow_ready_input},
        "StringReplace": {"Input": string_replace_input},
        "CalculateTotalEarnings": {"Input": calculate_total_earnings_input},
        "ConvertCsvToJson": {"Input": convert_csv_to_json_input}
    }
    return workflow_input
