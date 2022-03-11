"""Reads legal information from a json file and returns an object"""

import json
from pathlib import Path

def read_legal(path: Path = Path("static/text/legal.json")) -> dict:
    """Reads information from the legal. file and returns a dict
    
    Args:
        path (Path): path to the file to be read. Defaults to "static/text/legal.json"
    
    Returns:
        dict: dict containing the json content 
    """
    with path.open(encoding="utf-8", mode="r") as file:
        return json.load(file)