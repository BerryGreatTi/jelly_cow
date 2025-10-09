import os
import logging
import json
from datetime import datetime, timedelta


def initialize_loggers():
    os.makedirs("logs", exist_ok=True)
    with open("apis/logger_config.json", "r") as f:
        config = json.load(f)
    logging.config.dictConfig(config)