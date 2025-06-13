from pathlib import Path
import sys


def get_resource_path(relative_path):
    try:
        base_path = Path(sys._MEIPASS)
        return str(base_path / relative_path)
    except AttributeError:
        base_path = Path.cwd()
        return str(base_path / relative_path)
