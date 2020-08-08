import pytest

from source.check_workflow_ready import is_workflow_ready, is_sublist


@pytest.mark.parametrize(
    "list1, list2, expected_result",
    [
        ([], [], True),
        ([1], [], False),
        ([1], [1], True),
        ([1], [2], False),
        ([1], [1, 2], True),
        ([1, 2, 3], [4, 3, 2, 1], True)
    ]
)
def test_is_sublist(list1, list2, expected_result):
    assert is_sublist(list1, list2) == expected_result


@pytest.mark.parametrize(
    "files_present, required_files, expected_result",
    [
        ([], [], True),
        (["file1"], [], True),
        ([], ["file1"], False),
        (["file1"], ["file2"], False),
        (["file1", "file2"], ["file1", "file2"], True),
        (["file1", "file2"], ["file1"], True),
        (["file1"], ["file1", "file2"], False),
        (["file1", "file2", "file3"], ["file3", "file2", "file1"], True),
        (["file1", "file2", "file3"], ["file1", "file2"], True),
        (["file1", "file2", "file3"], ["file1", "file2", "File4"], False)
    ]
)
def test_is_workflow_ready(files_present, required_files, expected_result):
    files_present_info = {"Contents": list(map(lambda key: {"Key": key}, files_present))}
    print(files_present_info)
    assert is_workflow_ready(files_present_info, required_files) == expected_result
