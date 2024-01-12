# Tesseract-client documentation

## Introduction

Tesseract-client is a client for the Tesseract file-hosting service. It is written in Python 3 and uses the Tesseract API to communicate with the server.

## Installation

> `tesseract-client` requires Python 3.9 or higher.

Tesseract-client is available on PyPI and can be installed with pip:

```bash
pip install tesseract-client
```

> If you get an error during installation, make sure that you have the latest version of pip installed. You can upgrade pip with `pip install --upgrade pip`.

Verify that the installation was successful by running `tesseract --version`.

```bash
$ tesseract --version
tesseract 0.0.5
```

## Usage

```bash
usage: main.py [-h] [-V] [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}] {signup,login,logout,run,config,pull} ...
```

### Login

Before you can use the client, you must create an account on the Tesseract server. You can do this with the `signup` command:

```bash
tesseract signup [--username <username>] [--password <password>]
```

If you do not specify a username and password, you will be prompted for them.

After you have created an account, you can login with the `login` command:

```bash
tesseract login [--username <username>] [--password <password>]
```

It uses the keyring library to store your credentials in the system keyring. You will only need to login once, as the credentials will be stored for future use.

> **Note:** If you are using a Linux distribution that does not have the keyring library installed by default, you will need to install it manually. For example, on Ubuntu, you can install it with `sudo apt install gnome-keyring`.

If you wish to logout, you can use the `tesseract logout` command. It will also delete all the files associated with your account from the local directory.


### Configuring the client

By default, the client will create a directory called `tesseract` in your home directory, and will monitor this directory for changes. The local database file will be stored in `~/.local/share/tesseract/tesseract.db`.

You can change these defaults with the `config` command:

```bash
tesseract config [--path PATH] [--db DB] [--api_url API_URL]
```

By default, the client will use the default Tesseract API URL. If you are running your own instance of the Tesseract server, you can configure the client to use your own API URL.


### Pulling files

If you have used the Tesseract on another machine and want to pull the files from the server, or you just want to pull the latest version of the files, you can use the `pull` command:

```bash
tesseract pull
```

It will compare the files in the local directory with the files on the server, and download only parts of files that were modified since the last pull. If a file was deleted on the server, it will be deleted locally as well.


### Running the monitoring

To run the monitoring, you should use the `tesseract run` command. This will start the monitoring process, which will automatically upload any files that are added to or modified in the monitored directory. It will also upload to the server any files that were modified while the monitoring was not running and try to pull any files that were modified on the server.

```bash
tesseract run
```

## Uninstalling

If you wish to uninstall the client, you should consider running `tesseract logout` first. This will delete all the files associated with your account from the local directory.

After that, you can uninstall the client with pip:

```bash
pip uninstall tesseract-client
```
