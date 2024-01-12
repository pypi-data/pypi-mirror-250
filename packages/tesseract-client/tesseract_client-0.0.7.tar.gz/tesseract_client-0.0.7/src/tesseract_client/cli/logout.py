from loguru import logger

from tesseract_client.config import delete_credentials, clean_up


def logout():
    """Deletes the credentials from the config file and keyring and cleans up the file system"""
    try:
        clean_up()
    except FileNotFoundError:
        pass

    delete_credentials()
    logger.info("Logged out")
