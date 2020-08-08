def lambda_handler(event, context):
    pass


def replace_string(file_obj, to_replace: str, replace_with: str) -> str:
    file_contents = file_obj.read().decode("utf-8")
    return file_contents.replace(to_replace, replace_with)

