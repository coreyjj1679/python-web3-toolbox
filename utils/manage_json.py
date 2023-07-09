import os

def check_file_exists(filename: str, directory: str) -> bool:
    file_path = os.path.join(directory, filename)
    return os.path.isfile(file_path)

def get_unique_filename(filename: str, directory: str) -> str:
    base_filename, extension = os.path.splitext(filename)
    counter = 1

    while os.path.isfile(os.path.join(directory, filename)):
        filename = f"{base_filename}({counter}){extension}"
        counter += 1

    return filename