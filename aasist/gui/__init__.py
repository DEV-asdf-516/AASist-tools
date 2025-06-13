from pathlib import Path
import sys

current_dir = Path(__file__).parent
project_root = current_dir.parent

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# python -m gui.aasist_guidance.main
# python -m gui.aasist_test.main
