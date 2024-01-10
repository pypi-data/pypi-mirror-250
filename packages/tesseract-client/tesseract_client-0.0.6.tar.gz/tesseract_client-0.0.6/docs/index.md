# Tesseract-client documentation

## Introduction

Tesseract-client is a client for the [Tesseract]() file-hosting service. It is written in Python 3 and uses the [Tesseract API]() to communicate with the server.

## Installation

`tesseract-client` requires Python 3.9 or higher.

Tesseract-client is available on PyPI and can be installed with pip:

```bash
pip install tesseract-client
```

Verify that the installation was successful by running `tesseract --version`.

```bash
$ tesseract --version
tesseract 0.0.5
```

## Usage

### Login

Before you can use the client, you must login with your Tesseract credentials. You can do this with the `login` command:

```bash
tesseract login --username <username> --password <password>
```

If you do not specify a username and password, you will be prompted for them.

It uses the keyring library to store your credentials in the system keyring. You will only need to login once, as the credentials will be stored for future use.


### Running the monitoring

To run the monitoring, you can use the `tesseract run` command. This will start the monitoring process, which will automatically upload any files that are added to or modified in the monitored directory.

```bash
tesseract run [--path PATH] [--db DB] [--api_url API_URL]
```

The `--path` option specifies the path to the directory to monitor. If not specified, the `~/tesseract` directory will be used.

The `--db` option specifies the path where the database file will be stored. If not specified, the `~/.local/share/tesseract/tesseract.db` file will be used.

The `--api_url` option specifies the URL of the Tesseract API. If not specified, the default URL will be used.


### Pulling files

To pull files from the server, you can use the `tesseract pull` command. This will download all the updated files.

```bash
tesseract pull
```