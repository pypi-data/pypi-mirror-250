import getpass
from loguru import logger

from tesseract_client.api_manager import APIManager, API_URL
from tesseract_client.config import get_config


def signup(username: str = None, password: str = None):
    """Sign the user up for a new account"""
    if username is None:
        username = input('Username: ')
    if password is None:
        password = getpass.getpass('Password: ')

    _, _, api_url = get_config()
    api_manager = APIManager(
        username=username,
        password=password,
        api_urls=API_URL(api_url)
    )
    api_manager.signup()
    logger.info(f"Created account for {username}")
