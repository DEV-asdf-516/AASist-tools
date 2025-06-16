import subprocess
import sys


def run_module(module_name):
    subprocess.run([sys.executable, "-m", module_name])


def main():
    if len(sys.argv) < 2:
        print("Usage: aasist-run <guidance | test | one>")
        sys.exit(1)

    mode = sys.argv[1].lower()

    modules = {
        "guidance": "aasist.src.gui.aasist_guidance.main",
        "test": "aasist.src.gui.aasist_test.main",
        "one": "aasist.src.gui.aasist_one.main",
    }

    if mode in modules:
        run_module(modules[mode])
        sys.exit(1)
    else:
        print(f"Unknown mode: {mode}. Available modes: {', '.join(modules.keys())}")
        sys.exit(1)


if __name__ == "__main__":
    main()
