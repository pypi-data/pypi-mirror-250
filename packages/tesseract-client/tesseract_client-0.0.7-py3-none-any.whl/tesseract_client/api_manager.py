import functools
import requests
from loguru import logger
from dataclasses import dataclass

from tesseract_client.file import Chunk, File


class InvalidCredentials(Exception):
    pass


class ServerError(Exception):
    def __init__(self, msg="Server error"):
        super().__init__(msg)


class NotFoundError(Exception):
    def __init__(self):
        super().__init__("Not found")


@dataclass
class API_URL:
    base: str

    @property
    def signup(self) -> str:
        return self.base + '/auth/signup'

    @property
    def login(self) -> str:
        return self.base + '/auth/signin'

    @property
    def get_chunk_size(self) -> str:
        return self.base + '/chunk/size'

    @property
    def upload_file(self) -> str:
        return self.base + '/file'

    @property
    def delete_file(self) -> str:
        return self.base + '/file'

    @property
    def get_file(self) -> str:
        return self.base + '/file'

    @property
    def get_files(self) -> str:
        return self.base + '/file/all'

    @property
    def get_file_chunks(self) -> str:
        return self.base + '/file/chunks'

    @property
    def upload_chunk(self) -> str:
        return self.base + '/chunk'

    @property
    def delete_chunk(self) -> str:
        return self.base + '/chunk'

    @property
    def get_chunk(self) -> str:
        return self.base + '/chunk'

    @property
    def get_chunk_url(self) -> str:
        return self.base + '/chunk/download'


class APIManager:
    """Handles communication with the server"""
    def __init__(self, username: str, password: str, api_urls: API_URL):
        self.access_token = None
        self.username = username
        self.password = password
        self.api_urls = api_urls

    def signup(self):
        """Signs up to the server"""
        response = requests.post(
            self.api_urls.signup,
            data={"username": self.username, "password": self.password}
        )
        if response.status_code == 201:
            return response.json()
        elif response.status_code == 400:
            logger.error("Username already exists")
            raise InvalidCredentials("Username already exists")
        elif response.status_code == 500:
            logger.error("Server error")
            raise ServerError()

    def login(self):
        """Logs in to the server and stores the access token"""
        try:
            response = requests.post(
                self.api_urls.login,
                data={"username": self.username, "password": self.password}
            )
        except requests.exceptions.ConnectionError:
            raise ServerError()
        if response.status_code == 200:
            self.access_token = response.json()["access_token"]
            logger.debug("Obtained access token")
        elif response.status_code == 401:
            logger.error("Invalid credentials")
            raise InvalidCredentials("Invalid credentials")
        elif response.status_code == 404:
            logger.error("User not found")
            raise NotFoundError()
        else:
            logger.error("Server error")
            raise ServerError()

    def renew_token(func):
        """Decorator that renews the access token if it has expired"""
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except InvalidCredentials:
                logger.debug("Access token expired. Renewing...")
                self.login()
                return func(self, *args, **kwargs)
        return wrapper

    @renew_token
    def _make_request(
        self,
        method: requests.Request,
        url: str,
        status_code: int,
        **kwargs
    ) -> requests.Response:
        """Makes a request to the server"""
        try:
            response = method(
                url,
                headers={"Authorization": f"Bearer {self.access_token}"},
                **kwargs
            )
        except requests.exceptions.ConnectionError:
            logger.error("Could not connect to server")
            raise ServerError("Could not connect to server")
        if response.status_code == status_code:
            return response
        if response.status_code == 401:
            raise InvalidCredentials("Invalid access token")
        elif response.status_code == 404:
            logger.error("Resource not found")
            raise NotFoundError()
        else:
            logger.error("Server error")
            raise ServerError()

    def get_chunk_size(self) -> int:
        """Gets the chunk size from the server"""
        return self._make_request(
            requests.get,
            self.api_urls.get_chunk_size,
            status_code=200
        ).json()

    def upload_file(self, file: File) -> None:
        """Uploads a file to the server"""
        self._make_request(
            requests.post,
            self.api_urls.upload_file,
            status_code=201,
            params={"path": file.file_path, "hash": file.hash}
        )

    def update_file(self, file: File) -> None:
        """Updates a file on the server"""
        self._make_request(
            requests.put,
            self.api_urls.upload_file,
            status_code=200,
            params={"path": file.file_path, "hash": file.hash}
        )

    def delete_file(self, file_path: str) -> None:
        """Deletes a file from the server"""
        self._make_request(
            requests.delete,
            self.api_urls.delete_file,
            status_code=204,
            params={"path": file_path}
        )

    def get_file(self, file_path: str) -> File:
        """Gets the metadata of a file from the server"""
        file = self._make_request(
            requests.get,
            self.api_urls.get_file,
            status_code=200,
            params={"path": file_path}
        ).json()
        return File(file['path'], file['hash'])

    def get_files(self) -> list[File]:
        """Gets all files from the server"""
        files = self._make_request(
            requests.get,
            self.api_urls.get_files,
            status_code=200
        ).json()
        return [File(file['path'], file['hash']) for file in files]

    def get_file_chunks(self, file_path: str) -> list[Chunk]:
        """Gets all chunks of a file from the server"""
        chunks = self._make_request(
            requests.get,
            self.api_urls.get_file_chunks,
            status_code=200,
            params={"path": file_path}
        ).json()
        return [Chunk(chunk['file_path'], chunk['order'], chunk['hash']) for chunk in chunks]

    def upload_chunk(self, chunk: Chunk, data: bytes) -> None:
        """Uploads a chunk to the server"""
        self._make_request(
            requests.post,
            self.api_urls.upload_chunk,
            status_code=201,
            params={
                "file_path": chunk.file_path,
                "order": chunk.order,
                "hash": chunk.hash
            },
            files={"file": data, }
        )

    def update_chunk(self, chunk: Chunk, data: bytes) -> None:
        """Updates a chunk on the server"""
        self._make_request(
            requests.put,
            self.api_urls.upload_chunk,
            status_code=200,
            params={
                "file_path": chunk.file_path,
                "order": chunk.order,
                "hash": chunk.hash
            },
            files={"file": data}
        )

    def delete_chunk(self, file_path: str, order: int) -> None:
        """Deletes a chunk from the server"""
        self._make_request(
            requests.delete,
            self.api_urls.delete_chunk,
            status_code=204,
            params={
                "file_path": file_path,
                "order": order
            }
        )

    def get_chunk_meta(self, file_path: str, order: int) -> Chunk:
        """Gets the metadata of a chunk from the server"""
        chunk = self._make_request(
            requests.get,
            self.api_urls.get_chunk,
            status_code=200,
            params={
                "file_path": file_path,
                "order": order
            }
        ).json()
        return Chunk(chunk['file_path'], chunk['order'], chunk['hash'])

    def download_chunk(self, file_path: str, order: int) -> bytes:
        """Downloads a chunk from the server"""
        url = self._make_request(
            requests.get,
            self.api_urls.get_chunk_url,
            status_code=200,
            params={
                "file_path": file_path,
                "order": order
            }
        ).json()['url']
        return requests.get(url).content


if __name__ == '__main__':
    api_manager = APIManager('test', 'test', API_URL('http://localhost:8000'))
    api_manager.login()
    print(api_manager.access_token)
