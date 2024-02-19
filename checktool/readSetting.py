import yaml
from box import Box
import os
import logging
from loguru import logger
from logging.handlers import RotatingFileHandler


def ReadConfig(logger) -> Box:
    confFile = os.path.join(os.path.dirname(__file__), "config.yml")
    with open(os.path.normpath(confFile), mode="r", encoding="utf-8") as yml:
        config: dict = yaml.safe_load(yml)

    logger.debug(f"config: {config}")
    return Box(config, default_box=True)


def logging():
    handler = RotatingFileHandler("file.log", maxBytes=5000, backupCount=3)
    logger.add(handler)
    logger.info("start logging")
    return logger
