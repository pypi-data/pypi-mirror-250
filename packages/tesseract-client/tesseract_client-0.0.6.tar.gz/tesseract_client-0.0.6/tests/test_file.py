import os
import math
import hashlib
from hypothesis import (
    given,
    settings,
    HealthCheck,
    strategies as st
)

from tests.utils import write_to_file, append_to_file, replace_in_file
from tesseract_client.file import File
from tesseract_client.chunk import Chunk, ChunkAction


def get_chunks(file_path: str, file: File, chunk_size: int) -> list[Chunk]:
    with open(file_path, 'rb') as f:
        return file.split_into_chunks(f, chunk_size)


def test_get_file_hash(tmpdir):
    file_content = b"Test Content"
    file_path = os.path.join(tmpdir, "test_file.txt")
    with open(file_path, 'wb') as f:
        f.write(file_content)

    expected_hash = hashlib.sha256(file_content).hexdigest()
    assert File.get_file_hash(file_path) == expected_hash


def test_get_relative_path():
    subdir = "subdir"
    file_path = os.path.join(subdir, "test_file.txt")
    assert File.get_relative_path(file_path, subdir) == "test_file.txt"
    assert File.get_relative_path(file_path, subdir + "/") == "test_file.txt"
    file_path = os.path.join(subdir, subdir, "test_file.txt")
    assert File.get_relative_path(file_path, subdir) == f"{subdir}/test_file.txt"
    subdir = '/home/user/subdir'
    file_path = os.path.join(subdir, "test_file.txt")
    assert File.get_relative_path(file_path, subdir) == "test_file.txt"


def test_from_local_file(tmpdir):
    file_path = os.path.join(tmpdir, "test_file.txt")
    write_to_file(file_path, b"Test Content")
    file = File.from_local_file(file_path, tmpdir)
    assert file.file_path == "test_file.txt"
    assert file.hash == File.get_file_hash(file_path)


@settings(suppress_health_check=(HealthCheck.function_scoped_fixture,))
@given(
    chunk_size=st.integers(min_value=1, max_value=1000),
    content=st.binary()
)
def test_split_into_chunks(tmpdir, chunk_size, content):
    file_path = os.path.join(tmpdir, "test_file.txt")
    write_to_file(file_path, content)
    file = File.from_local_file(file_path, tmpdir)
    with open(file_path, 'rb') as f:
        chunks = file.split_into_chunks(f, chunk_size)

    expected_chunk_count = math.ceil(len(content) / chunk_size)
    assert len(chunks) == expected_chunk_count

    # Split content into chunks of size chunk_size
    contents = [
        content[i:i + chunk_size] for i in range(0, len(content), chunk_size)
    ]

    order = 1
    for (chunk, data), expected_content in zip(chunks, contents):
        assert chunk.file_path == "test_file.txt"
        assert chunk.hash == hashlib.sha256(data).hexdigest()
        assert chunk.order == order
        assert data == expected_content
        order += 1


def test_get_updated_chunks_no_changes(tmpdir):
    file_path = os.path.join(tmpdir, "test_file.txt")
    content = b"test content"

    # Create file
    write_to_file(file_path, content)
    file = File.from_local_file(file_path, tmpdir)
    chunks = [chunk[0] for chunk in get_chunks(file_path, file, 1000)]

    # Update file
    with open(file_path, 'rb') as f:
        updated_chunks = file.get_updated_chunks(f, chunks, 1000)
    assert len(updated_chunks) == 0


def test_get_updated_chunks_new_chunks(tmpdir):
    file_path = os.path.join(tmpdir, "test_file.txt")
    content = b""

    # Create file
    write_to_file(file_path, content)
    file = File.from_local_file(file_path, tmpdir)
    chunks = [chunk[0] for chunk in get_chunks(file_path, file, 1000)]

    # Update file
    new_content = b"0123456789"
    append_to_file(file_path, new_content)
    with open(file_path, 'rb') as f:
        updated_chunks = file.get_updated_chunks(f, chunks, 10)

    assert len(updated_chunks) == 1
    assert updated_chunks[0][0][0].order == 1
    assert updated_chunks[0][0][0].hash == hashlib.sha256(new_content).hexdigest()
    assert updated_chunks[0][1] == ChunkAction.CREATE

    chunks = [chunk[0] for chunk in get_chunks(file_path, file, 1000)]

    # Append new chunk
    new_content = b"0123456789"
    append_to_file(file_path, content + new_content)
    with open(file_path, 'rb') as f:
        updated_chunks = file.get_updated_chunks(f, chunks, 10)

    assert len(updated_chunks) == 1
    assert updated_chunks[0][0][0].order == 2
    assert updated_chunks[0][0][0].hash == hashlib.sha256(new_content).hexdigest()
    assert updated_chunks[0][1] == ChunkAction.CREATE


def test_get_updated_chunks_deleted_chunks(tmpdir):
    file_path = os.path.join(tmpdir, "test_file.txt")
    content = b"0123456789"

    # Create file
    write_to_file(file_path, content)
    file = File.from_local_file(file_path, tmpdir)
    chunks = [chunk[0] for chunk in get_chunks(file_path, file, 10)]

    # Delete chunk
    write_to_file(file_path, b"")
    with open(file_path, 'rb') as f:
        updated_chunks = file.get_updated_chunks(f, chunks, 10)

    assert len(updated_chunks) == 1
    assert updated_chunks[0][0][0].order == 1
    assert updated_chunks[0][0][1] is None
    assert updated_chunks[0][1] == ChunkAction.DELETE


def test_get_updated_chunks_updated_chunks(tmpdir):
    file_path = os.path.join(tmpdir, "test_file.txt")
    content = b"0123456789"

    # Create file
    write_to_file(file_path, content)
    file = File(file_path, str(tmpdir))
    chunks = [chunk[0] for chunk in get_chunks(file_path, file, 10)]

    # Update chunk
    new_content = b"9876543210"
    replace_in_file(file_path, 0, 10, new_content)
    with open(file_path, 'rb') as f:
        updated_chunks = file.get_updated_chunks(f, chunks, 10)

    assert len(updated_chunks) == 1
    assert updated_chunks[0][0][0].order == 1
    assert updated_chunks[0][0][0].hash == hashlib.sha256(new_content).hexdigest()
    assert updated_chunks[0][1] == ChunkAction.UPDATE


def test_get_updated_chunks_multiple_changes(tmpdir):
    file_path = os.path.join(tmpdir, "test_file.txt")
    content = b"0123456789"

    # Create file
    write_to_file(file_path, content)
    file = File(file_path, str(tmpdir))
    chunks = [chunk[0] for chunk in get_chunks(file_path, file, 10)]

    # Update chunk
    new_content = b"9876543210"
    write_to_file(file_path, new_content)
    with open(file_path, 'rb') as f:
        updated_chunks = file.get_updated_chunks(f, chunks, 10)

    assert len(updated_chunks) == 1
    assert updated_chunks[0][0][0].order == 1
    assert updated_chunks[0][0][0].hash == hashlib.sha256(new_content).hexdigest()
    assert updated_chunks[0][1] == ChunkAction.UPDATE

    chunks = [chunk[0] for chunk in get_chunks(file_path, file, 10)]

    # Delete chunk
    write_to_file(file_path, b"")
    with open(file_path, 'rb') as f:
        updated_chunks = file.get_updated_chunks(f, chunks, 10)

    assert len(updated_chunks) == 1
    assert updated_chunks[0][0][0].order == 1
    assert updated_chunks[0][0][1] is None
    assert updated_chunks[0][1] == ChunkAction.DELETE

    chunks = [chunk[0] for chunk in get_chunks(file_path, file, 10)]

    # Append new chunk
    new_content = b"0123456789"
    write_to_file(file_path, new_content)
    with open(file_path, 'rb') as f:
        updated_chunks = file.get_updated_chunks(f, chunks, 10)

    assert len(updated_chunks) == 1
    assert updated_chunks[0][0][0].order == 1
    assert updated_chunks[0][0][0].hash == hashlib.sha256(new_content).hexdigest()
    assert updated_chunks[0][1] == ChunkAction.CREATE


def test_get_updated_chunks_updated_in_middle(tmpdir):
    file_path = os.path.join(tmpdir, "test_file.txt")
    content = b"0123456789"

    # Create file
    write_to_file(file_path, content)
    file = File(file_path, str(tmpdir))
    chunks = [chunk[0] for chunk in get_chunks(file_path, file, 2)]

    # Update chunk with the same size
    replace_in_file(file_path, 2, 4, b"21")
    with open(file_path, 'rb') as f:
        updated_chunks = file.get_updated_chunks(f, chunks, 2)
    assert len(updated_chunks) == 1
    assert updated_chunks[0][0][0].order == 2
    assert updated_chunks[0][0][0].hash == hashlib.sha256(b"21").hexdigest()
    assert updated_chunks[0][1] == ChunkAction.UPDATE

    chunks = [chunk[0] for chunk in get_chunks(file_path, file, 2)]

    # Update chunk with a different size
    replace_in_file(file_path, 2, 4, b"3210")
    with open(file_path, 'rb') as f:
        updated_chunks = file.get_updated_chunks(f, chunks, 2)
    # 01 21 45 67 89 -> 01 32 10 45 67 89
    assert len(updated_chunks) == 5
    print(updated_chunks)
    assert updated_chunks[0][0][0].order == 6
    assert updated_chunks[0][0][1] == b"89"
    assert updated_chunks[0][1] == ChunkAction.CREATE
    assert updated_chunks[1][0][0].order == 2
    assert updated_chunks[1][0][1] == b"32"
    assert updated_chunks[1][1] == ChunkAction.UPDATE
    assert updated_chunks[2][0][0].order == 3
    assert updated_chunks[2][0][1] == b"10"
    assert updated_chunks[2][1] == ChunkAction.UPDATE
    assert updated_chunks[3][0][0].order == 4
    assert updated_chunks[3][0][1] == b"45"
    assert updated_chunks[3][1] == ChunkAction.UPDATE
    assert updated_chunks[4][0][0].order == 5
    assert updated_chunks[4][0][1] == b"67"
    assert updated_chunks[4][1] == ChunkAction.UPDATE
