import pandas as pd
import boto3


def lambda_handler(event, _):
    s3_client = boto3.client("s3")
    people_file = s3_client.get_object(Bucket=event["InputBucket"], Key=event["PeopleKey"])["Body"]
    jobs_file = s3_client.get_object(Bucket=event["InputBucket"], Key=event["JobsKey"])["Body"]
    people_df = pd.read_csv(people_file)
    jobs_df = pd.read_csv(jobs_file)
    transformed_csv_data = calculate_total_earnings(people_df, jobs_df).to_csv(index=False).encode("utf-8")
    s3_client.put_object(Bucket=event["OutputBucket"], Key=event["OutputKey"], Body=transformed_csv_data)


def calculate_total_earnings(people_df: pd.DataFrame, jobs_df: pd.DataFrame) -> pd.DataFrame:
    people_and_jobs = pd.merge(people_df, jobs_df, on=["COMPANY", "JOB"])
    people_and_jobs["TOTAL_EARNINGS"] = people_and_jobs["MONTHS_WORKED"] * people_and_jobs["SALARY"]
    return people_and_jobs.drop(columns=["REQUIRED_SKILLS", "SALARY"])

