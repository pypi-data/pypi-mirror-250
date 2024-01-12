import pytest
import tempfile
import os
import sqlite3

from tesseract_client.file import File
from tesseract_client.chunk import Chunk
from tesseract_client.db_manager import DBManager


@pytest.fixture
def db_manager() -> DBManager:
    """Creates a temporary database and returns a DBManager instance"""
    db_fd, db_path = tempfile.mkstemp()
    with DBManager(db_path) as db:
        yield db
    os.close(db_fd)
    os.unlink(db_path)


def test_create_file(db_manager: DBManager):
    file = File(file_path='/path/to/file.txt', hash='file_hash')
    db_manager.create_file(file)

    retrieved_file = db_manager.get_file_by_path('/path/to/file.txt')
    assert retrieved_file.file_path == '/path/to/file.txt'
    assert retrieved_file.hash == 'file_hash'


def test_create_chunk(db_manager: DBManager):
    chunk = Chunk(file_path='/path/to/file.txt', order=1, hash='chunk_hash')
    db_manager.create_chunk(chunk)

    chunks = db_manager.get_chunks('/path/to/file.txt')
    assert len(chunks) == 1
    retrieved_chunk = chunks[0]
    assert retrieved_chunk.file_path == '/path/to/file.txt'
    assert retrieved_chunk.order == 1
    assert retrieved_chunk.hash == 'chunk_hash'


def test_update_file(db_manager: DBManager):
    file = File(file_path='/path/to/file.txt', hash='file_hash')
    db_manager.create_file(file)

    updated_file = File(file_path='/path/to/file.txt', hash='new_file_hash')
    db_manager.update_file(updated_file)

    retrieved_file = db_manager.get_file_by_path('/path/to/file.txt')
    assert retrieved_file.file_path == '/path/to/file.txt'
    assert retrieved_file.hash == 'new_file_hash'


def test_update_chunk(db_manager: DBManager):
    chunk = Chunk(file_path='/path/to/file.txt', order=1, hash='chunk_hash')
    db_manager.create_chunk(chunk)

    updated_chunk = Chunk(
        file_path='/path/to/file.txt',
        order=1,
        hash='new_chunk_hash'
    )
    db_manager.update_chunk(updated_chunk)

    chunks = db_manager.get_chunks('/path/to/file.txt')
    assert len(chunks) == 1
    retrieved_chunk = chunks[0]
    assert retrieved_chunk.file_path == '/path/to/file.txt'
    assert retrieved_chunk.order == 1
    assert retrieved_chunk.hash == 'new_chunk_hash'


def test_delete_file(db_manager: DBManager):
    file = File(file_path='/path/to/file.txt', hash='file_hash')
    db_manager.create_file(file)

    db_manager.delete_file('/path/to/file.txt')

    retrieved_file = db_manager.get_file_by_path('/path/to/file.txt')
    assert retrieved_file is None


def test_delete_chunk(db_manager: DBManager):
    chunk = Chunk(file_path='/path/to/file.txt', order=1, hash='chunk_hash')
    db_manager.create_chunk(chunk)

    db_manager.delete_chunk(chunk.file_path, chunk.order)

    chunks = db_manager.get_chunks('/path/to/file.txt')
    assert len(chunks) == 0


def test_get_files(db_manager: DBManager):
    file1 = File(file_path='/path/to/file1.txt', hash='file1_hash')
    file2 = File(file_path='/path/to/file2.txt', hash='file2_hash')
    db_manager.create_file(file1)
    db_manager.create_file(file2)

    files = db_manager.get_files()
    assert len(files) == 2
    assert files[0].file_path == '/path/to/file1.txt'
    assert files[0].hash == 'file1_hash'
    assert files[1].file_path == '/path/to/file2.txt'
    assert files[1].hash == 'file2_hash'


def test_get_chunks(db_manager: DBManager):
    chunk1 = Chunk(file_path='/path/to/file.txt', order=1, hash='chunk1_hash')
    chunk2 = Chunk(file_path='/path/to/file.txt', order=2, hash='chunk2_hash')
    db_manager.create_chunk(chunk1)
    db_manager.create_chunk(chunk2)

    chunks = db_manager.get_chunks('/path/to/file.txt')
    assert len(chunks) == 2
    assert chunks[0].file_path == '/path/to/file.txt'
    assert chunks[0].order == 1
    assert chunks[0].hash == 'chunk1_hash'
    assert chunks[1].file_path == '/path/to/file.txt'
    assert chunks[1].order == 2
    assert chunks[1].hash == 'chunk2_hash'


def test_get_file_by_path(db_manager: DBManager):
    file = File(file_path='/path/to/file.txt', hash='file_hash')
    db_manager.create_file(file)

    retrieved_file = db_manager.get_file_by_path('/path/to/file.txt')
    assert retrieved_file.file_path == '/path/to/file.txt'
    assert retrieved_file.hash == 'file_hash'


def test_get_file_by_path_returns_none_if_not_found(db_manager: DBManager):
    retrieved_file = db_manager.get_file_by_path('/path/to/file.txt')
    assert retrieved_file is None


def test_file_name_unique(db_manager: DBManager):
    file1 = File(file_path='/path/to/file.txt', hash='file_hash')
    file2 = File(file_path='/path/to/file.txt', hash='file_hash')
    db_manager.create_file(file1)
    with pytest.raises(sqlite3.IntegrityError):
        db_manager.create_file(file2)


def test_chunk_unique(db_manager: DBManager):
    chunk1 = Chunk(file_path='/path/to/file.txt', order=1, hash='chunk_hash')
    chunk2 = Chunk(file_path='/path/to/file.txt', order=1, hash='chunk_hash1')
    db_manager.create_chunk(chunk1)
    with pytest.raises(sqlite3.IntegrityError):
        db_manager.create_chunk(chunk2)
