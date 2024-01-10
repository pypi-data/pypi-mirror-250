import pytest
from pathlib import Path

from tesseract_client import (
    DEFAULT_INDEX_PATH,
    DEFAULT_DB_PATH,
    DEFAULT_API_URL,
)
from tesseract_client.config import (
    create_default_config_if_not_exists,
    update_config,
    get_config,
    store_credentials,
    get_credentials,
    delete_credentials,
    clean_up,
    NoCredentialsError
)


def test_create_default_config_if_not_exists(monkeypatch, tmpdir):
    mock_config_path = tmpdir.join('config').join('config.ini')
    monkeypatch.setattr('tesseract_client.config.CONFIG_PATH', str(mock_config_path))

    create_default_config_if_not_exists()

    with open(str(mock_config_path), 'r') as configfile:
        assert configfile.read().strip() == (
            '[CONFIG]\n'
            f'index_path = {DEFAULT_INDEX_PATH}\n'
            f'db_path = {DEFAULT_DB_PATH}\n'
            f'api_url = {DEFAULT_API_URL}'
        )


def test_update_config(monkeypatch, tmpdir):
    mock_config_path = tmpdir.join('config').join('config.ini')
    monkeypatch.setattr('tesseract_client.config.CONFIG_PATH', str(mock_config_path))

    create_default_config_if_not_exists()

    update_config(
        index_path='new_index_path',
        db_path='new_db_path',
        api_url='new_api_url'
    )

    with open(str(mock_config_path), 'r') as configfile:
        assert configfile.read().strip() == (
            '[CONFIG]\n'
            'index_path = new_index_path\n'
            'db_path = new_db_path\n'
            'api_url = new_api_url'
        )


def test_get_config(monkeypatch, tmpdir):
    mock_config_path = tmpdir.join('config').join('config.ini')
    monkeypatch.setattr('tesseract_client.config.CONFIG_PATH', str(mock_config_path))

    create_default_config_if_not_exists()

    assert get_config() == (
        DEFAULT_INDEX_PATH,
        DEFAULT_DB_PATH,
        DEFAULT_API_URL
    )


def test_store_credentials(monkeypatch, tmpdir, mocker):
    mock_keyring = mocker.patch('keyring.set_password')

    mock_config_path = tmpdir.join("config").join('config.ini')
    monkeypatch.setattr('tesseract_client.config.CONFIG_PATH', str(mock_config_path))

    create_default_config_if_not_exists()

    store_credentials('username', 'password')

    with open(str(mock_config_path), 'r') as configfile:
        config_content = configfile.read().strip()
        expected_content = (
            '[CONFIG]\n'
            f'index_path = {DEFAULT_INDEX_PATH}\n'
            f'db_path = {DEFAULT_DB_PATH}\n'
            f'api_url = {DEFAULT_API_URL}\n\n'
            '[CREDENTIALS]\n'
            'username = username'
        )
        assert config_content == expected_content

    mock_keyring.assert_called_once_with('tesseract', 'username', 'password')


def test_get_credentials(monkeypatch, tmpdir, mocker):
    mock_keyring_set = mocker.patch('keyring.set_password')
    mock_keyring_get = mocker.patch('keyring.get_password')

    mock_config_path = tmpdir.join('config').join('config.ini')
    monkeypatch.setattr('tesseract_client.config.CONFIG_PATH', str(mock_config_path))

    create_default_config_if_not_exists()
    store_credentials('username', 'password')
    mock_keyring_get.return_value = 'password'

    assert get_credentials() == ('username', 'password')
    mock_keyring_set.assert_called_once_with('tesseract', 'username', 'password')
    mock_keyring_get.assert_called_once_with('tesseract', 'username')


def test_delete_credentials(monkeypatch, tmpdir, mocker):
    mocker.patch('keyring.set_password')
    mocker.patch('keyring.get_password')
    mocker.patch('keyring.delete_password')

    mock_config_path = tmpdir.join('config').join('config.ini')
    monkeypatch.setattr('tesseract_client.config.CONFIG_PATH', str(mock_config_path))

    create_default_config_if_not_exists()
    store_credentials('username', 'password')

    delete_credentials()

    with open(str(mock_config_path), 'r') as configfile:
        assert configfile.read().strip() == (
            '[CONFIG]\n'
            f'index_path = {DEFAULT_INDEX_PATH}\n'
            f'db_path = {DEFAULT_DB_PATH}\n'
            f'api_url = {DEFAULT_API_URL}'
        )

    with pytest.raises(NoCredentialsError):
        get_credentials()


def test_clean_up(monkeypatch, tmpdir):
    mock_config_path = tmpdir.join('config').join('config.ini')
    mock_db_path = tmpdir.join('db').join('db.sqlite')
    mock_index_path = tmpdir.join('index')
    monkeypatch.setattr('tesseract_client.config.CONFIG_PATH', str(mock_config_path))

    create_default_config_if_not_exists()
    update_config(
        index_path=str(mock_index_path),
        db_path=str(mock_db_path)
    )

    # Create mock files
    Path(mock_db_path).parent.mkdir(parents=True)
    mock_db_path.write('')
    Path(mock_index_path).mkdir()

    assert Path(mock_db_path).exists()
    assert Path(mock_index_path).exists()

    clean_up()

    assert not Path(mock_db_path).exists()
    assert not Path(mock_index_path).exists()
