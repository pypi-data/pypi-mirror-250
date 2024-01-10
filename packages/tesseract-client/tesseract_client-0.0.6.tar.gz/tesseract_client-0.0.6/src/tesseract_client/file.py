import os
import hashlib
from pathlib import Path
from typing import TextIO
from loguru import logger

from tesseract_client.chunk import Chunk, ChunkAction


class File:
    """ Represents a file on the client machine. """
    def __init__(self, file_path: str, hash: str):
        self.file_path = file_path
        self.hash = hash
        logger.debug(f"Initialized File object for {file_path}")

    def split_into_chunks(
        self,
        fd: TextIO,
        chunk_size: int
    ) -> list[tuple[Chunk, bytes]]:
        """
        Returns a list of Chunk objects along with their data
        for the given file.
        """
        chunks = []
        chunk_num = 1
        while True:
            data = fd.read(chunk_size)
            if not data:
                break

            chunk_hash = hashlib.sha256(data).hexdigest()
            chunk = Chunk(
                file_path=self.file_path,
                order=chunk_num,
                hash=chunk_hash
            )
            chunks.append((chunk, data))
            chunk_num += 1
        logger.debug(f"Split {self.file_path} into {len(chunks)} chunks")
        return chunks

    def get_updated_chunks(
        self,
        fd: TextIO,
        indexed_chunks: list[Chunk],
        chunk_size: int
    ) -> list[tuple[Chunk, bytes], ChunkAction]:
        """
        Returns a list of chunks that have been updated since the last time
        the file was indexed.
        """
        chunks = self.split_into_chunks(fd, chunk_size)
        data = [chunk[1] for chunk in chunks]
        chunks = [chunk[0] for chunk in chunks]
        updated_chunks = Chunk.get_updated_chunks(indexed_chunks, chunks)
        result = []
        for chunk, action in updated_chunks:
            if action == ChunkAction.DELETE:
                result.append(((chunk, None), action))
            else:
                result.append(((chunk, data[chunk.order - 1]), action))
        return result

    @staticmethod
    def get_relative_path(file_path, root_folder) -> str:
        """Returns relative file path to the root folder"""
        relative_path = os.path.relpath(file_path, root_folder)
        logger.debug(f"Relative path for {file_path} is {relative_path}")
        return relative_path

    @staticmethod
    def get_file_hash(file_path: str) -> str:
        """Returns the hash of a file"""
        with open(file_path, 'rb') as file:
            file_hash = hashlib.sha256(file.read()).hexdigest()
        logger.debug(f"File hash for {file_path} is {file_hash}")
        return file_hash

    @staticmethod
    def create_folder_path_if_not_exists(path: str, is_file: bool) -> None:
        """ Create the full path to the folder if it doesn't exist """
        path = Path(path)
        if is_file:
            path = path.parent
        path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Created path to: {path}")

    @classmethod
    def from_local_file(cls, file_path: str, root_folder: str):
        """Returns a File object from an absolute file path"""
        logger.debug(f"Created File object from local file {file_path}")
        return cls(
            cls.get_relative_path(file_path, root_folder),
            cls.get_file_hash(file_path)
        )

    def __repr__(self):
        return f"File({self.file_path}, {self.hash})"

    def __eq__(self, other):
        return self.file_path == other.file_path and self.hash == other.hash
