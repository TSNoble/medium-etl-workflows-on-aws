from pathlib import Path

import pytest
import pandas as pd

from source.calculate_total_earnings import calculate_total_earnings, lambda_handler


DATA_DIR = Path(__file__).parent.parent.joinpath("data")


@pytest.mark.parametrize(
    "companies, jobs, skills, months_worked, salaries, expected_totals",
    [
        (["Foo"], ["a"], ["123"], [1], [1000], [1000]),
        (["Foo", "Bar"], ["a", "b"], ["123", "456"], [1, 2], [100, 200], [100, 400]),
        (["Foo", "Bar", "Baz"], ["a", "b", "c"], ["123", "456", "789"], [1, 2, 3], [10, 20, 30], [10, 40, 90])
    ]
)
def test_calculate_total_earnings(companies, jobs, skills, months_worked, salaries, expected_totals):
    people_df = pd.DataFrame({"COMPANY": companies, "JOB": jobs, "MONTHS_WORKED": months_worked})
    jobs_df = pd.DataFrame({"COMPANY": companies, "JOB": jobs, "SALARY": salaries, "REQUIRED_SKILLS": skills})
    expected_df = pd.DataFrame({"COMPANY": companies, "JOB": jobs, "MONTHS_WORKED": months_worked, "TOTAL_EARNINGS": expected_totals})
    actual_df = calculate_total_earnings(people_df, jobs_df)
    pd.testing.assert_frame_equal(actual_df, expected_df)


def test_lambda_handler(mock_s3):
    people_filepath = DATA_DIR.joinpath("people.csv").absolute()
    jobs_filepath = DATA_DIR.joinpath("jobs.csv").absolute()
    merged_filepath = DATA_DIR.joinpath("merged.csv").absolute()
    event = {
        "InputBucket": "MockInputBucket",
        "PeopleKey": "people.csv",
        "JobsKey": "jobs.csv",
        "OutputBucket": "MockOutputBucket",
        "OutputKey": "calculate_total_earnings/output_file.csv"
    }
    mock_s3.upload_file(Bucket=event["InputBucket"], Key=event["PeopleKey"], Filename=str(people_filepath))
    mock_s3.upload_file(Bucket=event["InputBucket"], Key=event["JobsKey"], Filename=str(jobs_filepath))
    lambda_handler(event, [])
    file_bytes = mock_s3.get_object(Bucket=event["OutputBucket"], Key=event["OutputKey"])["Body"]
    actual_output = pd.read_csv(file_bytes)
    expected_output = pd.read_csv(str(merged_filepath))
    pd.testing.assert_frame_equal(actual_output, expected_output)
