import logging


def get_logger() -> logging.Logger:
    format = "%(asctime)s - %(levelname)s - %(filename)s - %(message)s"
    logging.basicConfig(format=format)
    logger = logging.getLogger("Bug-Bounty-Automation")
    logger.setLevel("INFO")
    return logger
