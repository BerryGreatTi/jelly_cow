import logging
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        }
    },
    "loggers": {
        "jm.agent.handler": {"level": "DEBUG", "handlers": ["console"]},
        "jm.slack.handler": {"level": "DEBUG", "handlers": ["console"]},
    },
}


def initialize_loggers():
    """Initializes the loggers from the config dictionary."""
    logging.config.dictConfig(LOGGING_CONFIG)
