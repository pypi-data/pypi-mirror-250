import os
import shutil
from loguru import logger

from tesseract_client.config import get_config, update_config


def config(index_path=None, db_path=None, api_url=None):
    """Configure the client"""
    prev_index_path, prev_db_path, _ = get_config()

    # Move files to new locations
    if index_path is not None:
        index_path = os.path.expanduser(index_path)
        if index_path != prev_index_path:
            shutil.move(prev_index_path, index_path)
            logger.info(f"Moved indexed files from {prev_index_path} to {index_path}")
    if db_path is not None:
        db_path = os.path.expanduser(db_path)
        if db_path != prev_db_path:
            shutil.move(prev_db_path, db_path)
            logger.info(f"Moved database from {prev_db_path} to {db_path}")

    # Update config file
    update_config(index_path, db_path, api_url)
