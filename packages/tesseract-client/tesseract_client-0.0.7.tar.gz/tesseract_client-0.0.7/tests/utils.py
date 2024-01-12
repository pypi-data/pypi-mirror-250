import random
import string


def write_to_file(file_path: str, content: bytes) -> None:
    """Creates a sample file with the given content"""
    with open(file_path, 'wb') as file:
        file.write(content)


def append_to_file(file_path: str, content: bytes) -> None:
    """Appends the given content to the file"""
    with open(file_path, 'ab') as file:
        file.write(content)


def replace_in_file(file_path: str, start_index: int, end_index: int, content: bytes) -> None:
    """
    Replaces the content of the file from start_index (inclusive)
    to end_index (exclusive) with the given content.
    """
    with open(file_path, 'r+b') as file:
        text = file.read()
    text = text[:start_index] + content + text[end_index:]
    with open(file_path, 'wb') as file:
        file.write(text)


def generate_random_string(length: int) -> str:
    """Generates a random string of the given length"""
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))
