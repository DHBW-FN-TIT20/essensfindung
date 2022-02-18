import logging
from pathlib import Path

import yaml


def setup_logging(config_path: Path = Path("./logging.yml")):
    """Setup the Logger from the Config File - Only call once!"""
    if not config_path.exists:
        raise RuntimeWarning("No Logging Config Found!")

    with config_path.open(mode="r", encoding="utf-8") as config_file:
        logging_config = yaml.safe_load(config_file.read())

    logging_path = Path(logging_config.get("handlers").get("info_file_handler").get("filename"))
    logging_path.parent.mkdir(mode=666, parents=True, exist_ok=True)

    logging.config.dictConfig(logging_config)

    if logging_config:
        logging.config.dictConfig(logging_config)
    else:
        logging.basicConfig(level=logging.INFO)


logger = logging.getLogger("my_logger")
