import os
import math
import shutil
import hashlib
import tempfile
import pytest

from unittest.mock import Mock
from tesseract_client.api_manager import APIManager
from tesseract_client.db_manager import DBManager
from tesseract_client.services import Services
from tesseract_client.chunk import Chunk
from tests.utils import write_to_file, append_to_file, generate_random_string


INDEXED_FOLDER = "./indexed_folder"
CHUNK_SIZE = 10


@pytest.fixture
def services() -> Services:
    """Creates a temporary database and returns a Services instance"""
    db_fd, db_path = tempfile.mkstemp()
    os.mkdir(INDEXED_FOLDER)
    with DBManager(db_path) as db:
        api_manager = Mock(APIManager)
        yield Services(api_manager, db, INDEXED_FOLDER, CHUNK_SIZE)
    os.close(db_fd)
    os.unlink(db_path)
    shutil.rmtree(INDEXED_FOLDER)


def test_create_chunk(services: Services):
    chunk = Chunk("test_file.txt", 1, "test_hash")

    data = b"Test Content"
    services.create_chunk(chunk, data)

    indexed_chunks = services.db_manager.get_chunks("test_file.txt")
    assert len(indexed_chunks) == 1
    indexed_chunk = indexed_chunks[0]
    assert indexed_chunk.file_path == chunk.file_path
    assert indexed_chunk.order == chunk.order
    assert indexed_chunk.hash == chunk.hash
    services.api_manager.upload_chunk.assert_called_once()


def test_update_chunk(services: Services):
    chunk = Chunk("test_file.txt", 1, "test_hash")
    data = b"Test Content"
    services.create_chunk(chunk, data)
    services.api_manager.update_chunk.reset_mock()

    chunk.hash = "new_hash"
    data = b"New Content"
    services.update_chunk(chunk, data)

    indexed_chunks = services.db_manager.get_chunks("test_file.txt")
    assert len(indexed_chunks) == 1
    indexed_chunk = indexed_chunks[0]
    assert indexed_chunk.file_path == chunk.file_path
    assert indexed_chunk.order == chunk.order
    assert indexed_chunk.hash == chunk.hash
    services.api_manager.update_chunk.assert_called_once()


def test_delete_chunk(services: Services):
    chunk = Chunk("test_file.txt", 1, "test_hash")
    data = b"Test Content"
    services.create_chunk(chunk, data)
    services.api_manager.upload_chunk.reset_mock()

    services.delete_chunk(chunk)

    indexed_chunks = services.db_manager.get_chunks("test_file.txt")
    assert len(indexed_chunks) == 0
    services.api_manager.delete_chunk.assert_called_once()


def test_create_file(services: Services):
    file_path = os.path.join(INDEXED_FOLDER, "test_file.txt")
    content = b"Test Content"
    write_to_file(file_path, content)
    services.create_file(file_path)

    indexed_file = services.db_manager.get_file_by_path("test_file.txt")
    assert indexed_file.file_path == "test_file.txt"
    assert indexed_file.hash == hashlib.sha256(content).hexdigest()
    services.api_manager.upload_file.assert_called_once()
    indexed_chunks = services.db_manager.get_chunks("test_file.txt")
    assert len(indexed_chunks) == math.ceil(len(content) / CHUNK_SIZE)


def test_update_file_create_chunk(services: Services):
    file_path = os.path.join(INDEXED_FOLDER, "test_file.txt")
    content = bytes(generate_random_string(CHUNK_SIZE), 'utf-8')
    write_to_file(file_path, content)
    services.create_file(file_path)
    services.api_manager.update_file.reset_mock()
    services.api_manager.upload_chunk.reset_mock()

    append_to_file(file_path, content)
    services.update_file(file_path)

    indexed_file = services.db_manager.get_file_by_path("test_file.txt")

    assert indexed_file.file_path == "test_file.txt"
    assert indexed_file.hash == hashlib.sha256(content + content).hexdigest()
    services.api_manager.update_file.assert_called_once()
    assert services.api_manager.upload_chunk.call_count == 1
    indexed_chunks = services.db_manager.get_chunks("test_file.txt")
    assert len(indexed_chunks) == 2


def test_update_file_delete_chunk(services: Services):
    file_path = os.path.join(INDEXED_FOLDER, "test_file.txt")
    content = bytes(generate_random_string(CHUNK_SIZE), 'utf-8')
    write_to_file(file_path, content)
    services.create_file(file_path)
    services.api_manager.update_file.reset_mock()
    services.api_manager.upload_chunk.reset_mock()

    write_to_file(file_path, b"")
    services.update_file(file_path)

    indexed_file = services.db_manager.get_file_by_path("test_file.txt")

    assert indexed_file.file_path == "test_file.txt"
    assert indexed_file.hash == hashlib.sha256(b"").hexdigest()
    services.api_manager.update_file.assert_called_once()
    services.api_manager.delete_chunk.assert_called_once()
    indexed_chunks = services.db_manager.get_chunks("test_file.txt")
    assert len(indexed_chunks) == 0


def test_update_file_update_chunk(services: Services):
    file_path = os.path.join(INDEXED_FOLDER, "test_file.txt")
    content = bytes(generate_random_string(CHUNK_SIZE), 'utf-8')
    write_to_file(file_path, content)
    services.create_file(file_path)
    services.api_manager.update_file.reset_mock()
    services.api_manager.upload_chunk.reset_mock()

    append_to_file(file_path, content)
    services.update_file(file_path)

    indexed_file = services.db_manager.get_file_by_path("test_file.txt")

    assert indexed_file.file_path == "test_file.txt"
    assert indexed_file.hash == hashlib.sha256(content + content).hexdigest()
    services.api_manager.update_file.assert_called_once()
    services.api_manager.upload_chunk.assert_called_once()
    indexed_chunks = services.db_manager.get_chunks("test_file.txt")
    assert len(indexed_chunks) == 2


def test_delete_file(services: Services):
    file_path = os.path.join(INDEXED_FOLDER, "test_file.txt")
    content = b"Test Content"
    write_to_file(file_path, content)
    services.create_file(file_path)
    services.api_manager.upload_file.reset_mock()
    services.api_manager.upload_chunk.reset_mock()

    services.delete_file(file_path)

    indexed_file = services.db_manager.get_file_by_path("test_file.txt")
    assert indexed_file is None
    services.api_manager.delete_file.assert_called_once()
    indexed_chunks = services.db_manager.get_chunks("test_file.txt")
    assert len(indexed_chunks) == 0


def test_check_for_offline_changes(services: Services):
    file_path = os.path.join(INDEXED_FOLDER, "test_file.txt")
    content = b"Test Content"
    write_to_file(file_path, content)
    services.api_manager.upload_file.reset_mock()
    services.api_manager.upload_chunk.reset_mock()

    services.check_for_offline_changes()

    indexed_file = services.db_manager.get_file_by_path("test_file.txt")
    assert indexed_file.file_path == "test_file.txt"
    assert indexed_file.hash == hashlib.sha256(content).hexdigest()
    services.api_manager.upload_file.assert_called_once()
    indexed_chunks = services.db_manager.get_chunks("test_file.txt")
    assert len(indexed_chunks) == math.ceil(len(content) / CHUNK_SIZE)


def test_check_for_offline_deletions(services: Services):
    file_path = os.path.join(INDEXED_FOLDER, "test_file.txt")
    content = b"Test Content"
    write_to_file(file_path, content)
    services.create_file(file_path)
    services.api_manager.upload_file.reset_mock()
    services.api_manager.upload_chunk.reset_mock()

    os.remove(file_path)
    services.check_for_offline_changes()

    indexed_file = services.db_manager.get_file_by_path("test_file.txt")
    assert indexed_file is None
    services.api_manager.delete_file.assert_called_once()
    indexed_chunks = services.db_manager.get_chunks("test_file.txt")
    files = services.db_manager.get_files()
    assert len(indexed_chunks) == 0
    assert len(files) == 0


def test_check_for_offline_changes_no_changes(services: Services):
    file_path = os.path.join(INDEXED_FOLDER, "test_file.txt")
    content = b"Test Content"
    write_to_file(file_path, content)
    services.create_file(file_path)
    services.check_for_offline_changes()
    files = services.db_manager.get_files()
    assert len(files) == 1
    indexed_file = services.db_manager.get_file_by_path("test_file.txt")
    assert indexed_file is not None
