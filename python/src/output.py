import os
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


def get_dir(name):
    """
    Returns a path-like object to the directory with the given name inside the
    output directory. Creates the directory if it doesn't already exist.

    The name will be converted to a string if necessary.
    """
    dir = OUTPUT_DIR / str(name)
    os.makedirs(dir, exist_ok=True)
    return dir
