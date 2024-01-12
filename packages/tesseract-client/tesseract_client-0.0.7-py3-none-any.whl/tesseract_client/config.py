import os
import shutil
import keyring
import configparser
from pathlib import Path
from loguru import logger

from tesseract_client import (
    CONFIG_PATH
)


class NoCredentialsError(Exception):
    pass


def create_config_if_not_exists(index_path: str, db_path: str, api_url: str):
    """Create a config file if it doesn't exist"""
    path = Path(CONFIG_PATH)
    if path.exists():
        return
    path.parent.mkdir(parents=True)

    config = {
        'index_path': index_path,
        'db_path': db_path,
        'api_url': api_url
    }

    config_parser = configparser.ConfigParser()
    config_parser.read(CONFIG_PATH)
    config_parser['CONFIG'] = config
    with open(CONFIG_PATH, 'w') as configfile:
        config_parser.write(configfile)
    logger.debug(f"Created config file at {CONFIG_PATH}")


def update_config_file(
    index_path=None,
    db_path=None,
    api_url=None
):
    """Update the config file"""
    config_parser = configparser.ConfigParser()
    config_parser.read(CONFIG_PATH)
    if index_path is not None:
        config_parser['CONFIG']['index_path'] = index_path
        logger.debug(f"Updated index path in config file to {index_path}")
    if db_path is not None:
        config_parser['CONFIG']['db_path'] = db_path
        logger.debug(f"Updated db path in config file to {db_path}")
    if api_url is not None:
        config_parser['CONFIG']['api_url'] = api_url
        logger.debug(f"Updated API URL in config file to {api_url}")
    with open(CONFIG_PATH, 'w') as configfile:
        config_parser.write(configfile)


def update_config(
    index_path=None,
    db_path=None,
    api_url=None
):
    prev_index_path, prev_db_path, _ = get_config()

    # Move files to new locations
    if index_path is not None:
        index_path = os.path.expanduser(index_path)
        if index_path != prev_index_path:
            shutil.move(prev_index_path, index_path)
            logger.debug(f"Moved indexed files from {prev_index_path} to {index_path}")
    if db_path is not None:
        db_path = os.path.expanduser(db_path)
        if db_path != prev_db_path:
            shutil.move(prev_db_path, db_path)
            logger.debug(f"Moved database from {prev_db_path} to {db_path}")

    update_config_file(index_path, db_path, api_url)


def get_config() -> tuple[str, str, str]:
    """Get the index path, db path, and API URL from the config file"""
    config_parser = configparser.ConfigParser()
    config_parser.read(CONFIG_PATH)
    index_path = config_parser['CONFIG']['index_path']
    db_path = config_parser['CONFIG']['db_path']
    api_url = config_parser['CONFIG']['api_url']
    return index_path, db_path, api_url


def store_credentials(username: str, password: str):
    """Store the username and password in the config file and keyring"""
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    config['CREDENTIALS'] = {'username': username}
    with open(CONFIG_PATH, 'w') as configfile:
        config.write(configfile)
    try:
        keyring.set_password('tesseract', username, password)
        logger.info(f"Stored credentials for {username}")
    except keyring.errors.PasswordSetError:
        logger.error("Failed to store credentials")


def get_credentials() -> tuple[str, str]:
    """Get the username and password from the config file and keyring"""
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        username = config['CREDENTIALS']['username']
        password = keyring.get_password('tesseract', username)
        return username, password
    except KeyError:
        logger.error("No credentials found")
        raise NoCredentialsError


def delete_credentials():
    """Delete the username and password from the config file and keyring"""
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        username = config['CREDENTIALS']['username']
        config.remove_section('CREDENTIALS')
        with open(CONFIG_PATH, 'w') as configfile:
            config.write(configfile)
        keyring.delete_password('tesseract', username)
        logger.debug(f"Deleted credentials for {username}")
    except KeyError:
        logger.error("No credentials found")
        raise NoCredentialsError


def clean_up():
    """Delete the indexed folder and database"""
    index_path, db_path, _ = get_config()

    shutil.rmtree(index_path)
    logger.debug(f"Deleted indexed folder {index_path}")

    os.remove(db_path)
    logger.debug(f"Deleted database {db_path}")
