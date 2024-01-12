import pytest
from itertools import product
from responses import RequestsMock
from tesseract_client.api_manager import (
    APIManager,
    InvalidCredentials,
    ServerError,
    NotFoundError,
    API_URL
)
from tesseract_client.file import File
from tesseract_client.chunk import Chunk


@pytest.fixture
def api_manager():
    api_urls = API_URL("https://example.com")
    return APIManager("user", "pass", api_urls)


@pytest.fixture
def mock():
    with RequestsMock() as rsps:
        yield rsps


def test_signup_successful(api_manager: APIManager, mock: RequestsMock):
    mock.add(mock.POST, api_manager.api_urls.signup, status=200)
    api_manager.signup()


def test_signup_username_taken(api_manager: APIManager, mock: RequestsMock):
    mock.add(mock.POST, api_manager.api_urls.signup, status=400)

    with pytest.raises(InvalidCredentials):
        api_manager.signup()


def test_signup_server_error(api_manager: APIManager, mock: RequestsMock):
    mock.add(mock.POST, api_manager.api_urls.signup, status=500)

    with pytest.raises(ServerError):
        api_manager.signup()


def test_login_successful(api_manager: APIManager, mock: RequestsMock):
    mock.add(mock.POST, api_manager.api_urls.login, json={"access_token": "token123"}, status=200)
    api_manager.login()

    assert api_manager.access_token == "token123"


def test_login_invalid_credentials(api_manager: APIManager, mock: RequestsMock):
    mock.add(mock.POST, api_manager.api_urls.login, status=401)

    with pytest.raises(InvalidCredentials):
        api_manager.login()


def test_login_server_error(api_manager: APIManager, mock: RequestsMock):
    mock.add(mock.POST, api_manager.api_urls.login, status=500)

    with pytest.raises(ServerError):
        api_manager.login()


def test_login_not_found_error(api_manager: APIManager, mock: RequestsMock):
    mock.add(mock.POST, api_manager.api_urls.login, status=404)

    with pytest.raises(NotFoundError):
        api_manager.login()


def test_get_chunk_size(api_manager: APIManager, mock: RequestsMock):
    mock.add(mock.GET, api_manager.api_urls.get_chunk_size, body="1024", status=200)
    assert api_manager.get_chunk_size() == 1024


def test_upload_file(api_manager: APIManager, mock: RequestsMock):
    file = File("file.txt", "hash123")
    mock.add(mock.POST, api_manager.api_urls.upload_file, status=201)
    api_manager.upload_file(file)


def test_update_file(api_manager: APIManager, mock: RequestsMock):
    file = File("file.txt", "hash123")
    mock.add(mock.PUT, api_manager.api_urls.upload_file, status=200)
    api_manager.update_file(file)


def test_delete_file(api_manager: APIManager, mock: RequestsMock):
    mock.add(mock.DELETE, api_manager.api_urls.delete_file, status=204)
    api_manager.delete_file("file.txt")


def test_get_file(api_manager: APIManager, mock: RequestsMock):
    mock.add(mock.GET, api_manager.api_urls.get_file, json={"path": "file.txt", "hash": "hash123"}, status=200)
    file = api_manager.get_file("file.txt")

    assert file.file_path == "file.txt"
    assert file.hash == "hash123"


def test_get_files(api_manager: APIManager, mock: RequestsMock):
    mock.add(mock.GET, api_manager.api_urls.get_files, json=[{"path": "file.txt", "hash": "hash123"}], status=200)
    files = api_manager.get_files()

    assert len(files) == 1
    assert files[0].file_path == "file.txt"
    assert files[0].hash == "hash123"


def test_get_file_chunks(api_manager: APIManager, mock: RequestsMock):
    mock.add(mock.GET, api_manager.api_urls.get_file_chunks, json=[
        {"file_path": "file.txt",
         "order": 0,
         "hash": "hash123"}
    ], status=200)
    chunks = api_manager.get_file_chunks("file.txt")

    assert len(chunks) == 1
    assert chunks[0].file_path == "file.txt"
    assert chunks[0].order == 0
    assert chunks[0].hash == "hash123"


def test_upload_chunk(api_manager: APIManager, mock: RequestsMock):
    chunk = Chunk("file.txt", 0, "hash123")
    mock.add(mock.POST, api_manager.api_urls.upload_chunk, status=201)
    api_manager.upload_chunk(chunk, b"chunk data")


def test_update_chunk(api_manager: APIManager, mock: RequestsMock):
    chunk = Chunk("file.txt", 0, "hash123")
    mock.add(mock.PUT, api_manager.api_urls.upload_chunk, status=200)
    api_manager.update_chunk(chunk, b"chunk data")


def test_delete_chunk(api_manager: APIManager, mock: RequestsMock):
    mock.add(mock.DELETE, api_manager.api_urls.delete_chunk, status=204)
    api_manager.delete_chunk("file.txt", 0)


def test_get_chunk_meta(api_manager: APIManager, mock: RequestsMock):
    mock.add(mock.GET, api_manager.api_urls.get_chunk, json={
        "file_path": "file.txt",
        "order": 0,
        "hash": "hash123"
    }, status=200)
    chunk = api_manager.get_chunk_meta("file.txt", 0)

    assert chunk.file_path == "file.txt"
    assert chunk.order == 0
    assert chunk.hash == "hash123"


def test_download_chunk(api_manager: APIManager, mock: RequestsMock):
    mock.add(mock.GET, api_manager.api_urls.get_chunk_url, json={"url": "https://example.com/download"}, status=200)

    mock.add(mock.GET, "https://example.com/download", body=b"chunk data", status=200)
    data = api_manager.download_chunk("file.txt", 0)

    assert data == b"chunk data"


api_methods = [
    (lambda mngr: mngr.api_urls.get_chunk_size,
     lambda mock: mock.GET,
     lambda mngr: mngr.get_chunk_size, ()),

    (lambda mngr: mngr.api_urls.upload_file,
     lambda mock: mock.POST,
     lambda mngr: mngr.upload_file, (File("file.txt", "hash123"),)),

    (lambda mngr: mngr.api_urls.upload_file,
     lambda mock: mock.PUT,
     lambda mngr: mngr.update_file, (File("file.txt", "hash123"),)),

    (lambda mngr: mngr.api_urls.delete_file,
     lambda mock: mock.DELETE,
     lambda mngr: mngr.delete_file, ("file.txt",)),

    (lambda mngr: mngr.api_urls.get_file,
     lambda mock: mock.GET,
     lambda mngr: mngr.get_file, ("file.txt",)),

    (lambda mngr: mngr.api_urls.get_files,
     lambda mock: mock.GET,
     lambda mngr: mngr.get_files, ()),

    (lambda mngr: mngr.api_urls.get_file_chunks,
     lambda mock: mock.GET,
     lambda mngr: mngr.get_file_chunks, ("file.txt",)),

    (lambda mngr: mngr.api_urls.upload_chunk,
     lambda mock: mock.POST,
     lambda mngr: mngr.upload_chunk, (Chunk("file.txt", 0, "hash123"), b"chunk data")),

    (lambda mngr: mngr.api_urls.upload_chunk,
     lambda mock: mock.PUT,
     lambda mngr: mngr.update_chunk, (Chunk("file.txt", 0, "hash123"), b"chunk data")),

    (lambda mngr: mngr.api_urls.delete_chunk,
     lambda mock: mock.DELETE,
     lambda mngr: mngr.delete_chunk, ("file.txt", 0)),

    (lambda mngr: mngr.api_urls.get_chunk,
     lambda mock: mock.GET,
     lambda mngr: mngr.get_chunk_meta, ("file.txt", 0)),

    (lambda mngr: mngr.api_urls.get_chunk_url,
     lambda mock: mock.GET,
     lambda mngr: mngr.download_chunk, ("file.txt", 0)),
]


@pytest.mark.parametrize("url,method,function,args", api_methods)
def test_expired_token_renewed(
    api_manager: APIManager,
    mock: RequestsMock,
    url: callable,
    method: callable,
    function: callable,
    args: tuple
):
    mock.add(method(mock), url(api_manager), status=401)
    mock.add(mock.POST, api_manager.api_urls.login, json={"access_token": "token1234"}, status=200)

    with pytest.raises(InvalidCredentials):
        function(api_manager)(*args)

    assert api_manager.access_token == "token1234"


error_scenarios = [
    (404, NotFoundError),
    (500, ServerError),
]


@pytest.mark.parametrize("method_details,error_scenario", list(product(api_methods, error_scenarios)))
def test_api_methods_errors(api_manager: APIManager, mock: RequestsMock, method_details, error_scenario):
    url, method, function, args = method_details
    status_code, expected_exception = error_scenario

    mock.add(method(mock), url(api_manager), status=status_code)
    with pytest.raises(expected_exception):
        function(api_manager)(*args)
