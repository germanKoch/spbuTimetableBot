import app.config as config
import logging
import os


def config_logger():
    logging.basicConfig(level=os.environ.get("LOGLEVEL", config.LOGGING_LEVEL),
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
