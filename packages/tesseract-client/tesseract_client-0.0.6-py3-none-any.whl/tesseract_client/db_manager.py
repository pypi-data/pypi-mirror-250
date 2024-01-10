import sqlite3
from loguru import logger

from tesseract_client.file import File, Chunk


class DBManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        logger.debug(f"DBManager initialized with database path: {db_path}")

    def __enter__(self):
        self.db = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.db.cursor()
        self.init_db()
        logger.debug("Database connection established")
        return self

    def __exit__(self, *_):
        self.db.close()
        logger.debug("Database connection closed")

    def init_db(self):
        """Initializes the database tables if they don't already exist"""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS files (
                    file_path TEXT PRIMARY KEY,
                    hash TEXT NOT NULL
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS chunks (
                    file_path TEXT NOT NULL,
                    order_num INTEGER NOT NULL,
                    chunk_hash TEXT NOT NULL,
                    PRIMARY KEY (file_path, order_num),
                    FOREIGN KEY (file_path) REFERENCES files (file_path)
                )
            """)
            self.db.commit()
            logger.debug("Initialized database tables")
        except sqlite3.Error as e:
            logger.error(f"Error initializing database tables: {e}")
            raise

    def create_file(self, file: File):
        """Creates a file object in the database"""
        try:
            self.cursor.execute(
                "INSERT INTO files (file_path, hash) VALUES (?, ?)",
                (file.file_path, file.hash)
            )
            self.db.commit()
            logger.debug(f"File created in database: {file.file_path}")
        except sqlite3.Error as e:
            logger.error(f"Error creating file in database: {e}")
            raise

    def create_chunk(self, chunk: Chunk):
        """Creates a chunk object in the database"""
        try:
            self.cursor.execute(
                "INSERT INTO chunks (file_path, order_num, chunk_hash) VALUES (?, ?, ?)",
                (chunk.file_path, chunk.order, chunk.hash)
            )
            self.db.commit()
            logger.debug(f"Chunk created in database: {chunk.file_path} {chunk.order}")
        except sqlite3.Error as e:
            logger.error(f"Error creating chunk in database: {e}")
            raise

    def update_file(self, file: File):
        """Updates a file object in the database"""
        try:
            self.cursor.execute(
                "UPDATE files SET hash=? WHERE file_path=?",
                (file.hash, file.file_path)
            )
            self.db.commit()
            logger.debug(f"File updated in database: {file.file_path}")
        except sqlite3.Error as e:
            logger.error(f"Error updating file in database: {e}")
            raise

    def update_chunk(self, chunk: Chunk):
        """Updates a chunk object in the database"""
        try:
            self.cursor.execute(
                "UPDATE chunks SET chunk_hash=? WHERE file_path=? AND order_num=?",
                (chunk.hash, chunk.file_path, chunk.order)
            )
            self.db.commit()
            logger.debug(f"Chunk updated in database: {chunk.file_path} {chunk.order}")
        except sqlite3.Error as e:
            logger.error(f"Error updating chunk in database: {e}")
            raise

    def delete_file(self, file_path: str):
        """Deletes a file object from the database"""
        try:
            self.cursor.execute("DELETE FROM files WHERE file_path=?", (file_path, ))
            self.db.commit()
            logger.debug(f"File deleted from database: {file_path}")
        except sqlite3.Error as e:
            logger.error(f"Error deleting file from database: {e}")
            raise

    def delete_chunk(self, file_path: str, order: int):
        """Deletes a chunk object from the database"""
        try:
            self.cursor.execute(
                "DELETE FROM chunks WHERE file_path=? AND order_num=?",
                (file_path, order)
            )
            self.db.commit()
            logger.debug(f"Chunk deleted from database: {file_path} {order}")
        except sqlite3.Error as e:
            logger.error(f"Error deleting chunk from database: {e}")
            raise

    def get_chunks(self, file_path: str):
        """Gets all chunks for a file from the database"""
        try:
            self.cursor.execute(
                "SELECT file_path, order_num, chunk_hash FROM chunks WHERE file_path=?",
                (file_path, )
            )
            chunks = [
                Chunk(file_path=row[0], order=row[1], hash=row[2])
                for row in self.cursor.fetchall()
            ]
            logger.debug(f"Fetched chunks from database for file path: {file_path}")
            return chunks
        except sqlite3.Error as e:
            logger.error(f"Database error while fetching chunks: {e}")
            raise

    def get_files(self):
        """Gets all files from the database"""
        try:
            self.cursor.execute("SELECT file_path, hash FROM files")
            files = [
                File(file_path=row[0], hash=row[1])
                for row in self.cursor.fetchall()
            ]
            logger.debug("Fetched files from database")
            return files
        except sqlite3.Error as e:
            logger.error(f"Database error while fetching files: {e}")
            raise

    def get_file_by_path(self, file_path: str):
        """Gets a file from the database by file path"""
        try:
            self.cursor.execute(
                "SELECT file_path, hash FROM files WHERE file_path=?",
                (file_path, )
            )
            row = self.cursor.fetchone()
            if row is None:
                return None
            file = File(file_path=row[0], hash=row[1])
            logger.debug(f"Fetched file from database by path: {file_path}")
            return file
        except sqlite3.Error as e:
            logger.error(f"Database error while fetching file by path: {e}")
            raise
