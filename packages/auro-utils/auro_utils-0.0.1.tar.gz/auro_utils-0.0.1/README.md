# auro_utils

Auro Utils is a utility package offering various practical supports for the Auromix application, such as enhanced logging capabilities and more.

## Install

```bash
git clone https://github.com/Auromix/auro_utils
cd auro_utils
pip install -e .
```

## Test

```bash
cd auro_utils
python3 -m pytest -v .
```

## Usage

Following are some simplified examples of utilities offered by this package.

You can also find detailed examples in the `examples` folder.

```bash
cd auro_utils/examples
```

## Logger

### logger

Logger is a class that can be used to log messages to the console and to a file. It is a wrapper around loguru.

```python
from auro_utils.loggers.logger import Logger
my_logger = Logger()
my_logger.log_info("This is a info log test.")
```

### classic logger

Classic logger is a class that can be used to log messages to the console and to a file. It is a wrapper around the standard python logging module.

```python
from auro_utils.loggers.logger_classic import Logger
my_logger = Logger()
my_logger.log_info("This is a info log test.")
```

## Troubleshooting

### ModuleNotFoundError

Make sure you have installed the package correctly. See [Install](#install) section.

### Want to uninstall

```bash
pip uninstall auro_utils
```

## Contribute

Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for more information.
