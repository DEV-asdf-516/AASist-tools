from pathlib import Path
import sys


def get_resource_path(relative_path: Path):
    if hasattr(sys, "_MEIPASS"):
        return str(Path(sys._MEIPASS) / relative_path)
    else:
        return str(Path(__file__).resolve().parent.parent.parent.parent / relative_path)
