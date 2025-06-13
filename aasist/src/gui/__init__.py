from pathlib import Path
import sys


project_root = Path(__file__).parent.parent.parent.parent
src_path = project_root / "aasist" / "src"

if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# python -m aasist.src.gui.aasist_guidance.main
