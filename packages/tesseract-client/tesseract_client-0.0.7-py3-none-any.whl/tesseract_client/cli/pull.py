from loguru import logger

from tesseract_client.db_manager import DBManager
from tesseract_client.services import Services
from tesseract_client.api_manager import APIManager, API_URL
from tesseract_client.config import get_config, get_credentials, NoCredentialsError
from tesseract_client.cli.login import NotLoggedInError


def pull():
    """Pull updates from the server"""
    try:
        username, password = get_credentials()
    except NoCredentialsError:
        raise NotLoggedInError()

    indexed_folder, db_path, api_url = get_config()

    api_urls = API_URL(base=api_url)

    with DBManager(db_path) as db_manager:
        api_manager = APIManager(
            username=username,
            password=password,
            api_urls=api_urls
        )
        chunk_size = api_manager.get_chunk_size()
        services = Services(
            api_manager=api_manager,
            db_manager=db_manager,
            indexed_folder=indexed_folder,
            chunk_size=chunk_size
        )

        logger.info("Pulling updates from the server...")
        services.pull()
        logger.info("Finished pulling updates")
