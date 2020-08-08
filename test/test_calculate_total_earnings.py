import pytest
import pandas as pd

from source.calculate_total_earnings import calculate_total_earnings


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
