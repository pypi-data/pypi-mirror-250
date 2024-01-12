import pytest
from pathlib import Path

from tesseract_client.config import (
    create_config_if_not_exists,
    update_config_file,
    update_config,
    get_config,
    store_credentials,
    get_credentials,
    delete_credentials,
    clean_up,
    NoCredentialsError
)
from tesseract_client.file import File


def test_create_config_if_not_exists(monkeypatch, tmpdir):
    mock_config_path = tmpdir.join('config').join('config.ini')
    monkeypatch.setattr('tesseract_client.config.CONFIG_PATH', str(mock_config_path))

    index_path = str(tmpdir.join('index'))
    db_path = str(tmpdir.join('db').join('db.sqlite'))
    api_url = 'http://localhost:8000'

    create_config_if_not_exists(index_path, db_path, api_url)

    with open(str(mock_config_path), 'r') as configfile:
        assert configfile.read().strip() == (
            '[CONFIG]\n'
            f'index_path = {index_path}\n'
            f'db_path = {db_path}\n'
            f'api_url = {api_url}'
        )


def test_update_config_file(monkeypatch, tmpdir):
    mock_config_path = tmpdir.join('config').join('config.ini')
    monkeypatch.setattr('tesseract_client.config.CONFIG_PATH', str(mock_config_path))

    create_config_if_not_exists('index_path', 'db_path', 'api_url')

    update_config_file(
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


def test_update_config(monkeypatch, tmpdir):
    mock_config_path = tmpdir.join('config').join('config.ini')
    monkeypatch.setattr('tesseract_client.config.CONFIG_PATH', str(mock_config_path))

    index_path = str(tmpdir.join('index'))
    db_path = str(tmpdir.join('db.sqlite'))
    api_url = 'http://localhost:8000'

    create_config_if_not_exists(index_path, db_path, api_url)

    File.create_folder_path_if_not_exists(index_path, False)
    File.create_folder_path_if_not_exists(db_path, True)
    Path(db_path).touch()

    assert Path(index_path).exists()
    assert Path(db_path).exists()

    new_index_path = str(tmpdir.join('new_index'))
    new_db_path = str(tmpdir.join('new_db.sqlite'))
    new_api_url = 'http://localhost:8001'

    update_config(
        index_path=new_index_path,
        db_path=new_db_path,
        api_url=new_api_url
    )

    assert Path(index_path).exists() is False
    assert Path(db_path).exists() is False

    assert Path(new_index_path).exists()
    assert Path(new_db_path).exists()

    with open(str(mock_config_path), 'r') as configfile:
        assert configfile.read().strip() == (
            '[CONFIG]\n'
            f'index_path = {new_index_path}\n'
            f'db_path = {new_db_path}\n'
            f'api_url = {new_api_url}'
        )


def test_get_config(monkeypatch, tmpdir):
    mock_config_path = tmpdir.join('config').join('config.ini')
    monkeypatch.setattr('tesseract_client.config.CONFIG_PATH', str(mock_config_path))

    create_config_if_not_exists('index_path', 'db_path', 'api_url')

    assert get_config() == (
        'index_path',
        'db_path',
        'api_url'
    )


def test_store_credentials(monkeypatch, tmpdir, mocker):
    mock_keyring = mocker.patch('keyring.set_password')

    mock_config_path = tmpdir.join("config").join('config.ini')
    monkeypatch.setattr('tesseract_client.config.CONFIG_PATH', str(mock_config_path))

    create_config_if_not_exists('index_path', 'db_path', 'api_url')

    store_credentials('username', 'password')

    with open(str(mock_config_path), 'r') as configfile:
        config_content = configfile.read().strip()
        expected_content = (
            '[CONFIG]\n'
            'index_path = index_path\n'
            'db_path = db_path\n'
            'api_url = api_url\n\n'
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

    create_config_if_not_exists('index_path', 'db_path', 'api_url')
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

    create_config_if_not_exists('index_path', 'db_path', 'api_url')
    store_credentials('username', 'password')

    delete_credentials()

    with open(str(mock_config_path), 'r') as configfile:
        assert configfile.read().strip() == (
            '[CONFIG]\n'
            'index_path = index_path\n'
            'db_path = db_path\n'
            'api_url = api_url'
        )

    with pytest.raises(NoCredentialsError):
        get_credentials()


def test_clean_up(monkeypatch, tmpdir):
    mock_config_path = tmpdir.join('config').join('config.ini')
    mock_db_path = tmpdir.join('db').join('db.sqlite')
    mock_index_path = tmpdir.join('index')
    monkeypatch.setattr('tesseract_client.config.CONFIG_PATH', str(mock_config_path))

    create_config_if_not_exists('index_path', 'db_path', 'api_url')
    update_config_file(
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
