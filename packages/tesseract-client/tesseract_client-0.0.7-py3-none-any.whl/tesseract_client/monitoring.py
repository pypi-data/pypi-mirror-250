from watchdog.events import FileSystemEventHandler
from loguru import logger

from tesseract_client.services import Services


class FileChangeHandler(FileSystemEventHandler):
    """Handles changes in the monitored folder"""
    def __init__(self, services: Services):
        super().__init__()
        self.services = services
        logger.debug("FileChangeHandler object initialized")

    def on_created(self, event):
        if not event.is_directory:
            self.services.create_file(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.services.delete_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory and event.event_type == 'modified':
            self.services.update_file(event.src_path)
