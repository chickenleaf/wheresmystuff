# backend/app/utils/logging.py

import logging
import json
from datetime import datetime

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        return json.dumps(log_record)

def configure_logging():
    logger = logging.getLogger("lost_and_found")
    logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(JsonFormatter())

    # File handler
    file_handler = logging.FileHandler('lost_and_found.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(JsonFormatter())

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger