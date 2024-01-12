![logo](logo.png)
# Lognet
Lognet is a lightweight logging library for Python, designed to simplify the process of logging messages with different levels of severity. It provides an easy-to-use interface, customization options.

## Features
- Log Levels: Log messages with different severity levels, including DEBUG, INFO, WARNING, ERROR, and EXCEPTION.

- Convenient log message formatting

- Console and File Logging: Log messages to the console, a file, or both.

# Installation
Install Lognet Logger using pip:

```
pip install lognet
```
## ARCHITECTURE
```bash
lognet/
│
├── core/
│   ├── __init__.py
│   ├── application/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── handlers/
│   │   │   ├── handler.py
│   │   │   ├── file_handler.py
│   │   │   └── console_handler.py
│   │   ├── formatters/
│   │   │   └── log_formatter.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── log_levels.py
│   │   └── log_entity.py
│   ├── configuration/
│   │   ├── __init__.py
│   │   ├── handler_configurator.py
│   │   └── logger_config.py
```
## Usage
### Basic Example
```python
from lognet import Logger, LogLevel, LoggerConfig, ConsoleHandler, HandlerConfigurator


logger_config = LoggerConfig(min_level=LogLevel.DEBUG,
                             handler_configurator=HandlerConfigurator(console_handler=ConsoleHandler()))

logger = Logger(logger_config)

logger.log(level=LogLevel.INFO, message="Example log message")
```

### Change format
```python
from lognet import Logger, LogLevel, LoggerConfig, ConsoleHandler, HandlerConfigurator


logger_config = LoggerConfig(log_format="[{time}] [{log_level}] {message}",
                             min_level=LogLevel.DEBUG,
                             handler_configurator=HandlerConfigurator(console_handler=ConsoleHandler()))

logger = Logger(logger_config)

logger.log(level=LogLevel.INFO, message="Example log message")
logger.log(level=LogLevel.ERROR, message="Example error message")
```

### File Handler
```python
from lognet import Logger, LogLevel, LoggerConfig, HandlerConfigurator, FileHandler


logger_config = LoggerConfig(min_level=LogLevel.DEBUG,
                             handler_configurator=HandlerConfigurator(console_handler=FileHandler(file_name="log.txt")))

logger = Logger(logger_config)

logger.log(level=LogLevel.INFO, message="Example log message")
logger.log(level=LogLevel.ERROR, message="Example error message")
```
```

## Future updates
Ideas that I will try to implement
- multithreading
- async
- logging to database
- Filtration
- Settings for each message level separately
- Integration with metrics and tracing
- Support various output formats
- adding tags
- logging in json

## Connect with me/bug/request/suggestion
Check the FEEDBACK.md for information

## Documentation
Check the USAGE.md file for comprehensive examples and configuration details.

## Changelog
Review the CHANGELOG.md file for information on the latest updates and changes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
