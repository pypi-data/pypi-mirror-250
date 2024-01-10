# Py Encry <!-- omit in toc -->

[![Python](https://img.shields.io/badge/support-9101FF?logo=python&logoColor=FFDF58&labelColor=3D7AAB&label=Python%203.12)](https://www.python.org/downloads/release/python-3120/)&nbsp;&nbsp; [![Build Status](https://github.com/Py-Encry/py-encry/workflows/Tests/badge.svg)](https://github.com/Py-Encry/py-encry/actions/workflows/tests.yml)

Nti Johanneberg gymnasiearbete 2023/2024

## Description <!-- omit in toc -->

Py Encry is a library for encrypting and decrypting information in pictures.
The library offers a variety of different encryption methods, and also allows to combine them.
There is an API mode, which allows to use the library in other projects, and a CLI mode, which allows to use the library from the command line.
Additionally, the tool is accesable through our website.

## Table of Contents <!-- omit in toc -->

- [Installation](#installation)
- [Usage](#usage)
  - [CLI](#cli)
  - [API](#api)
- [Contributing](#contributing)
  - [Setup](#setup)
  - [Run tests](#run-tests)
- [License](#license)

## Installation

To install Py Encry, you need to have Python 3.12 or newer installed on your computer.
The library is available on [PyPI](https://pypi.org/project/py-encry/), so you can install it using pip.

```bash
python -m pip install py-encry
```

## Usage

To use Py Encry, you can either use the API or the CLI.
If the program is intended to be used in another project, the API is the way to go, the CLI is intended for quick usage from the command line.

### CLI

To use the CLI, you need to install the package and then run the `pyencry` command.
Note! The python package install folder may not be in your PATH, so you may need to add it manually.
Just google your operating system and how to add the python executable folder to your PATH.

Once the package is installed, you can run the `pyencry` command.
You can use the `--help` flag to get more information about all the available options.

```bash
pyencry -v
1.0.0b1

pyencry --help
...
```

### API

To use the API, you need to import the `py_encry` module.

```python
from pyencry import ImageHandler

handler = ImageHandler("<path_to_image>")
handler.encrypt("<encryption_method>", data="<data_to_encrypt>", key=<encryption_key>)
handler.save("<path_to_save_image>")
```

For full documentation, visit our website or check out the docstrings in the code.

## Contributing

If you want to contribute to Py Encry, you can do so by forking the repository and creating a pull request.
To build the project, you need to have Python 3.12 or newer installed on your computer and install the required packages.

### Setup

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required packages.

```bash
python -m pip install -r requirements.txt
```

### Run tests

```bash
python -m pytest
```

## License

[MIT](./LICENSE)
