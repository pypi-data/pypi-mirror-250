from loguru import logger
from watchdog.observers.polling import PollingObserver as Observer

from tesseract_client.db_manager import DBManager
from tesseract_client.services import Services
from tesseract_client.monitoring import FileChangeHandler
from tesseract_client.api_manager import APIManager, API_URL
from tesseract_client.config import get_config, get_credentials, NoCredentialsError
from tesseract_client.cli.login import NotLoggedInError


def run():
    """Start the monitoring process"""
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
        event_handler = FileChangeHandler(services)

        # Check for changes that were made while offline
        services.check_for_offline_changes()
        # Pull updates from the server
        services.pull()

        # Start monitoring the folder for changes
        observer = Observer()
        observer.schedule(
            event_handler,
            path=indexed_folder,
            recursive=True
        )
        observer.start()
        logger.info(f"Monitoring folder {indexed_folder} for updates...")

        try:
            while True:
                pass
        except KeyboardInterrupt:
            observer.stop()
            logger.info("Monitoring stopped due to KeyboardInterrupt")

        observer.join()
