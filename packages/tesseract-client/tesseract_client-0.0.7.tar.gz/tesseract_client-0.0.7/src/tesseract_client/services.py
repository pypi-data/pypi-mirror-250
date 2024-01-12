import os
from loguru import logger

from tesseract_client.api_manager import APIManager
from tesseract_client.db_manager import DBManager
from tesseract_client.file import File, Chunk, ChunkAction


class Services:
    """Provides business logic for the application"""
    def __init__(
        self,
        api_manager: APIManager,
        db_manager: DBManager,
        indexed_folder: str,
        chunk_size: int
    ):
        self.api_manager = api_manager
        self.db_manager = db_manager
        self.indexed_folder = indexed_folder
        self.chunk_size = chunk_size
        logger.debug("Services object initialized")

    def create_file(self, file_path: str):
        """Creates a new file in the database and uploads it to the server"""
        logger.info(f"File created: {file_path}")
        file = File.from_local_file(file_path, self.indexed_folder)
        self.db_manager.create_file(file)
        self.api_manager.upload_file(file)
        with open(file_path, 'rb') as fd:
            chunks = file.split_into_chunks(fd, self.chunk_size)
        for chunk, data in chunks:
            self.create_chunk(chunk, data)

    def update_file(self, file_path: str):
        """
        Updates an existing file in the database and uploads it to the server.
        """
        file = File.from_local_file(file_path, self.indexed_folder)
        indexed_file = self.db_manager.get_file_by_path(
            file.file_path
        )
        # Check if the file was actually modified
        if indexed_file.hash == file.hash:
            return
        logger.info(f"File updated: {file_path}")
        self.db_manager.update_file(file)
        self.api_manager.update_file(file)
        indexed_chunks = self.db_manager.get_chunks(file.file_path)
        with open(file_path, 'rb') as fd:
            updated_chunks = file.get_updated_chunks(
                fd,
                indexed_chunks,
                self.chunk_size,
            )
        logger.info(f"Found {len(updated_chunks)} updated chunks")
        for (chunk, data), action in updated_chunks:
            if action == ChunkAction.CREATE:
                self.create_chunk(chunk, data)
            elif action == ChunkAction.DELETE:
                self.delete_chunk(chunk)
            else:
                self.update_chunk(chunk, data)

    def delete_file(self, file_path: str):
        """Deletes a file from the database and the server"""
        path = File.get_relative_path(file_path, self.indexed_folder)
        chunks = self.db_manager.get_chunks(path)
        self.db_manager.delete_file(path)
        self.api_manager.delete_file(path)
        for chunk in chunks:
            self.delete_chunk(chunk)
        logger.info(f"File deleted: {file_path}")

    def create_chunk(self, chunk: Chunk, data: bytes):
        """Creates a new chunk in the database and uploads it to the server"""
        self.db_manager.create_chunk(chunk)
        self.api_manager.upload_chunk(chunk, data)

    def update_chunk(self, chunk: Chunk, data: bytes):
        """
        Updates an existing chunk in the database and uploads it to the server.
        """
        self.db_manager.update_chunk(chunk)
        self.api_manager.update_chunk(chunk, data)

    def delete_chunk(self, chunk: Chunk):
        """Deletes a chunk from the database and the server"""
        self.db_manager.delete_chunk(chunk.file_path, chunk.order)
        self.api_manager.delete_chunk(chunk.file_path, chunk.order)

    def check_for_offline_changes(self):
        """Checks for changes that were made while offline"""
        logger.debug("Checking for offline changes")
        self._check_for_offline_deletions()
        self._check_for_offline_updates(self.indexed_folder)

    def _check_for_offline_deletions(self):
        """Checks for files that were deleted while offline"""
        folder = self.indexed_folder
        db_files = self.db_manager.get_files()
        local_files = []
        for root, _, files in os.walk(folder):
            for file in files:
                file = os.path.join(root, file)
                file = File.get_relative_path(file, folder)
                local_files.append(file)
        for db_file in db_files:
            if db_file.file_path not in local_files:
                logger.info(f"File deleted while offline: {db_file.file_path}")
                self.delete_file(os.path.join(folder, db_file.file_path))

    def _check_for_offline_updates(self, folder: str = None):
        """Checks for files that were created/modified while offline"""
        for file in os.listdir(folder):
            file = os.path.join(folder, file)
            if os.path.isdir(file):
                self._check_for_offline_updates(file)
            else:
                db_file = self.db_manager.get_file_by_path(
                    File.get_relative_path(file, self.indexed_folder)
                )
                if db_file:
                    if db_file.hash != File.get_file_hash(file):
                        logger.info(f"File updated while offline: {file}")
                        self.update_file(file)
                else:
                    logger.info(f"File created while offline: {file}")
                    self.create_file(file)

    def pull(self):
        """Pulls the latest changes from the server"""
        logger.debug("Pulling latest changes from the server")
        files = self.api_manager.get_files()
        for file in files:
            db_file = self.db_manager.get_file_by_path(file.file_path)
            if db_file:
                if db_file.hash != file.hash:
                    logger.info(f"File updated on server: {file.file_path}")
                    self._update_file_from_server(file)
            else:
                logger.info(f"File created on server: {file.file_path}")
                self._create_file_from_server(file)
        self._check_for_server_deletions(files)

    def _create_file_from_server(self, file: File):
        """Creates a file from the server"""
        self.db_manager.create_file(file)
        open(os.path.join(self.indexed_folder, file.file_path), 'w').close()
        chunks = self.api_manager.get_file_chunks(file.file_path)
        for chunk in chunks:
            self.db_manager.create_chunk(chunk)
            data = self.api_manager.download_chunk(chunk.file_path, chunk.order)
            with open(os.path.join(self.indexed_folder, file.file_path), 'ab') as fd:
                fd.write(data)

    def _update_file_from_server(self, file: File):
        # TODO
        """Updates a file from the server"""
        server_chunks = self.api_manager.get_file_chunks(file.file_path)
        db_chunks = self.db_manager.get_chunks(file.file_path)

        # Update database
        updated_chunks = Chunk.get_updated_chunks(db_chunks, server_chunks)
        for chunk, action in updated_chunks:
            if action == ChunkAction.CREATE:
                self.db_manager.create_chunk(chunk)
            elif action == ChunkAction.DELETE:
                self.db_manager.delete_chunk(chunk.file_path, chunk.order)
            else:
                self.db_manager.update_chunk(chunk)

        # Update file
        with open(os.path.join(self.indexed_folder, file.file_path), 'rb') as fd:
            chunks = file.split_into_chunks(fd, self.chunk_size)
        db_chunk_data = [chunk[1] for chunk in chunks]
        db_chunk_hashes = [chunk.hash for chunk in db_chunks]
        chunk_data = []
        for chunk in server_chunks:
            if chunk.hash not in db_chunk_hashes:
                data = self.api_manager.download_chunk(chunk.file_path, chunk.order)
                chunk_data.append(data)
            else:
                chunk_data.append(db_chunk_data[db_chunk_hashes.index(chunk.hash)])
        with open(os.path.join(self.indexed_folder, file.file_path), 'wb') as fd:
            for data in chunk_data:
                fd.write(data)

    def _check_for_server_deletions(self, files: list[File]):
        """Checks for files that were deleted on the server"""
        db_files = self.db_manager.get_files()
        for db_file in db_files:
            if db_file not in files:
                logger.info(f"File deleted on server: {db_file.file_path}")
                self._delete_file_locally(db_file.file_path)

    def _delete_file_locally(self, file_path: str):
        """Deletes a file locally"""
        chunks = self.db_manager.get_chunks(file_path)
        self.db_manager.delete_file(file_path)
        for chunk in chunks:
            self.db_manager.delete_chunk(chunk.file_path, chunk.order)
        os.remove(os.path.join(self.indexed_folder, file_path))
