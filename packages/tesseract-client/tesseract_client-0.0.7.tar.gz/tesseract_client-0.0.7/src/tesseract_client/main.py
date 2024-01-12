import sys
import argparse


from importlib.metadata import version

from loguru import logger

from tesseract_client import DEFAULT_INDEX_PATH, DEFAULT_DB_PATH, DEFAULT_API_URL
from tesseract_client.file import File
from tesseract_client.config import create_config_if_not_exists, get_config
from tesseract_client.cli.login import login
from tesseract_client.cli.run import run
from tesseract_client.cli.config import config
from tesseract_client.cli.signup import signup
from tesseract_client.cli.logout import logout
from tesseract_client.cli.pull import pull


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-V',
        '--version',
        action='version',
        version=f'Tesseract {version(__package__)}'
    )

    parser.add_argument(
        '--log-level',
        help='Log level',
        type=str.upper,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    )
    subparsers = parser.add_subparsers(dest='command')

    # Signup
    signup_parser = subparsers.add_parser('signup', help='Create a new account')
    signup_parser.add_argument(
        '--username',
        '-u',
        help='Username to use for authentication',
        type=str
    )
    signup_parser.add_argument(
        '--password',
        '-p',
        help='Password to use for authentication',
        type=str
    )

    # Login
    login_parser = subparsers.add_parser('login', help='Login to the API')
    login_parser.add_argument(
        '--username',
        '-u',
        help='Username to use for authentication',
        type=str
    )
    login_parser.add_argument(
        '--password',
        '-p',
        help='Password to use for authentication',
        type=str
    )

    # Logout
    subparsers.add_parser('logout', help='Logout of the API')

    # Run
    subparsers.add_parser('run', help='Start monitoring')

    # Config
    config_parser = subparsers.add_parser('config', help='Configure Tesseract')
    config_parser.add_argument(
        '--path',
        help='Folder to index',
        type=str,
        default=None
    )
    config_parser.add_argument(
        '--db',
        help='Path to database file',
        type=str,
        default=None
    )
    config_parser.add_argument(
        '--api_url',
        help='URL of the API',
        type=str,
        default=None
    )

    # Pull
    subparsers.add_parser('pull', help='Pull files from the server')

    args = parser.parse_args()

    logger.remove()
    logger.add(
        sys.stdout,
        level=args.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>"
    )

    create_config_if_not_exists(DEFAULT_INDEX_PATH, DEFAULT_DB_PATH, DEFAULT_API_URL)
    indexed_folder, db_path, _ = get_config()

    File.create_folder_path_if_not_exists(indexed_folder, False)
    File.create_folder_path_if_not_exists(db_path, True)

    if args.command == 'signup':
        signup(args.username, args.password)
    elif args.command == 'login':
        login(args.username, args.password)
    elif args.command == 'logout':
        logout()
    elif args.command == 'run':
        run()
    elif args.command == 'config':
        config(args.path, args.db, args.api_url)
    elif args.command == 'pull':
        pull()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
