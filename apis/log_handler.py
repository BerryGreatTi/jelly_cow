import os
import logging
from datetime import datetime, timedelta


loggers = [
    "jm.agent.handler",
    "jm.slack.handler",
]

os.mkdir("logs", exist_ok=True)
log_path = f"logs/server.log"
log_level = os.getenv("LOG_LEVEL", "INFO")

def set_loggers():
    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        handler = logging.Handlers.RotatingFileHandler(log_path, maxBytes=1024 * 1024 * 10, backupCount=10)
        handler.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)