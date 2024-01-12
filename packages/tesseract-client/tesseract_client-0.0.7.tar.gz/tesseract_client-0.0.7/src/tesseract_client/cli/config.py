from loguru import logger

from tesseract_client.config import update_config


def config(index_path=None, db_path=None, api_url=None):
    """Configure the client"""
    if index_path or db_path or api_url:
        update_config(index_path, db_path, api_url)
        logger.info("Updated config file")
    else:
        logger.info("No changes made to config file")
