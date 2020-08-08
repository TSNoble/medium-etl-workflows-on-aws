import pandas as pd


def lambda_handler(event, context):
    pass


def calculate_total_earnings(people_df: pd.DataFrame, jobs_df: pd.DataFrame) -> pd.DataFrame:
    people_and_jobs = pd.merge(people_df, jobs_df, on=["COMPANY", "JOB"])
    people_and_jobs["TOTAL_EARNINGS"] = people_and_jobs["MONTHS_WORKED"] * people_and_jobs["SALARY"]
    return people_and_jobs.drop(columns=["REQUIRED_SKILLS", "SALARY"])

