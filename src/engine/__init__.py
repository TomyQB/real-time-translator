import configparser
import logging
import logging.config
import os
import sys
from datetime import datetime


def init_logging(app_name: str) -> logging.Logger:
    class AppFilter(logging.Filter):
        def filter(self, record):
            record.system_name = app_name
            record.level_name = record.levelname
            record.system_type = "MainLogger"
            record.event_at = datetime.now().isoformat()
            return True

    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'consoleFormatter': {
                'format': '%(asctime)s | %(levelname)-8s | %(filename)s-%(funcName)s-%(lineno)04d | %(message)s'
            },
        },
        'handlers': {
            'consoleHandler': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'consoleFormatter',
                'stream': sys.stdout,
            },
        },
        'loggers': {
            'root': {
                'level': 'DEBUG',
                'handlers': ['consoleHandler'],
            },
            'MainLogger': {
                'level': 'DEBUG',
                'handlers': ['consoleHandler'],
                'propagate': False,
                'qualname': 'MainLogger',
            },
        }
    }

    logging.config.dictConfig(logging_config)
    logger = logging.getLogger('MainLogger')
    logger.addFilter(AppFilter())

    logger.debug("Logging initialized")
    return logger


def get_config(config_file_name: str) -> configparser.ConfigParser:
    filename = "config.ini"
    config = configparser.ConfigParser()

    config_dir = os.path.join(config_file_name if os.path.exists(config_file_name) else '.', 'config')

    path_file = os.path.join(config_dir, filename)
    config.read(path_file)
    return config
