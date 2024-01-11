import os


def warm_up_path(path):
    # check if file exists, change file attribute for overwriting
    if os.path.isfile(path):
        os.chmod(path, 0o644)
        return True
    else:
        _, fileExtension = os.path.splitext(path)
        if fileExtension:
            path = os.path.dirname(path)
        os.makedirs(path, exist_ok=True)
        return False
