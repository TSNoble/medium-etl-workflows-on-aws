from source.generate_workflow_input import lambda_handler

import pytest


@pytest.fixture
def mock_environment(monkeypatch):
    monkeypatch.setenv("InputBucketName", "MockInput")
    monkeypatch.setenv("ProcessingBucketName", "MockProcessing")
    monkeypatch.setenv("OutputBucketName", "MockOutput")


def test_lambda_handler(mock_environment):
    results = lambda_handler({}, {})
    expected = {
        "CheckWorkflowReady": {
            "Input": {
                "InputBucket": "MockInput",
                "RequiredFiles": ["people.csv", "jobs.csv"]
            }
        },
        "StringReplace": {
            "Input": [
                {
                    "InputBucket": "MockInput",
                    "InputKey": "people.csv",
                    "ToReplace": "Programming",
                    "ReplaceWith": "Coding",
                    "OutputBucket": "MockProcessing",
                    "OutputKey": "string_replace/people.csv"
                },
                {
                    "InputBucket": "MockInput",
                    "InputKey": "jobs.csv",
                    "ToReplace": "Programming",
                    "ReplaceWith": "Coding",
                    "OutputBucket": "MockProcessing",
                    "OutputKey": "string_replace/jobs.csv"
                }
            ]
        },
        "CalculateTotalEarnings": {
            "Input": {
                "InputBucket": "MockProcessing",
                "PeopleKey": "string_replace/people.csv",
                "JobsKey": "string_replace/jobs.csv",
                "OutputBucket": "MockProcessing",
                "OutputKey": "calculate_total_earnings/merged.csv"
            }
        },
        "ConvertCsvToJson": {
            "Input": {
                "InputBucket": "MockProcessing",
                "InputKey": "calculate_total_earnings/merged.csv",
                "OutputBucket": "MockOutput",
                "OutputKey": "output.json"
            }
        }
    }
    assert results == expected
