import subprocess
import sys
from pathlib import Path
from typing import Any
from tqdm import tqdm


def get_resource_path(relative_path):
    try:
        base_path = Path(sys._MEIPASS)
        return str(base_path / relative_path)
    except AttributeError:
        base_path = Path.cwd()
        return str(base_path / relative_path)


class GUIBuilder:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GUIBuilder, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.project_root = Path.cwd()
        self.dist_path = self.project_root / "dist"
        self.build_path = self.project_root / "build"

        self.modules = {
            "guidance": {
                "entry": "gui/aasist_guidance/main.py",
                "name": "AASist_Guidance",
                "icon": "icons/guidance.ico",
                "resources": ["custom_theme.json", "icons/guidance.ico"],
            },
            "test": {
                "entry": "gui/aasist_test/main.py",
                "name": "AASist_Test",
                "icon": "icons/test.ico",
                "resources": ["custom_theme.json", "icons/test.ico"],
            },
            "one": {
                "entry": "gui/aasist_one/main.py",
                "name": "AASist_One",
                # "icon": "icons/integration.ico",
                "resources": ["custom_theme.json"],
            },
        }
        self._stages = {
            "INFO: PyInstaller": "running PyInstaller ...",
            "INFO: Initializing": "module initalizing ...",
            "INFO: Including": "including hooks ...",
            "INFO: checking": "checking validation ...",
            "INFO: Building": "building exe ...",
            "complete": "wait completed ...",
        }
        self._initialized = True

    def clean_build_folders(self):
        if self.build_path.exists():
            import shutil

            shutil.rmtree(self.build_path)

        for spec_file in self.project_root.glob("*.spec"):
            spec_file.unlink()

    def build_module(self, module_name, config: dict[str, Any]):

        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            f"--name={config['name']}",
            f"--distpath={self.dist_path}",
            f"--workpath={self.build_path}/{module_name}",
            "--clean",
        ]

        if config.get("icon") and Path(config["icon"]).exists():
            cmd.extend(["--icon", config["icon"]])

        for resource in config.get("resources", []):
            if not Path(resource).exists():
                continue
            if Path(resource).is_dir():
                cmd.extend(["--add-data", f"{resource};{resource}"])
            elif Path(resource).is_file():
                parent_dir = Path(resource).parent
                if str(parent_dir) == ".":
                    cmd.extend(["--add-data", f"{resource};."])
                else:
                    cmd.extend(["--add-data", f"{resource};{parent_dir}/"])

        hidden_imports = [
            "customtkinter",
            "tkinter",
            "PIL",
            "darkdetect",
            "packaging",
            "packaging.version",
            "packaging.specifiers",
        ]
        for lib in hidden_imports:
            cmd.extend(["--hidden-import", lib])

        cmd.append(config["entry"])

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=0,
                text=True,
                universal_newlines=True,
            )
            self._process_output(process, module_name)
        except subprocess.CalledProcessError as e:
            return e.stderr

    def build_all(self):

        self.clean_build_folders()

        self.dist_path.mkdir(exist_ok=True)

        for module_name, config in self.modules.items():
            self.build_module(module_name, config)

        self._list_exe_files()

    def _list_exe_files(self):
        for exe_file in self.dist_path.glob("*.exe"):
            size_mb = exe_file.stat().st_size / (1024 * 1024)
            print(f"  • {exe_file.name} ({size_mb:.1f} MB)")

    def _process_output(self, process: subprocess.Popen, module_name: str):
        module_name = f"{module_name:<16}"
        with tqdm(
            total=100,
            desc=f"{module_name} | {'start building...':<30}",
            bar_format="{desc} | {bar} | {percentage:2.0f}%",
            leave=True,
        ) as progress:
            failed = False
            for line in process.stdout:

                if progress.n < 99:
                    progress.n += 0.3
                    progress.refresh()
                if any(keyword in str(line).lower() for keyword in ["error", "failed"]):
                    failed = True
                    break
                for log, desc_ in self._stages.items():
                    if log in line:
                        progress.n = progress.n + 10 if progress.n < 90 else progress.n
                        progress.set_description_str(f"{module_name} | {desc_:<30}")
                        progress.refresh()
                        break

            process.wait()

            if failed:
                progress.set_description_str(
                    f"\033[91m{module_name}\033[0m | \033[91m{'build failed':<30}\033[0m"
                )
            else:
                progress.n = 100
                progress.set_description_str(
                    f"{module_name} | {'build completed successfully!':<30}"
                )


def main():
    builder = GUIBuilder()

    if len(sys.argv) > 1:
        module_name = sys.argv[1]
        if module_name in builder.modules:
            builder.build_module(module_name, builder.modules[module_name])
        else:
            print(f"사용 가능한 모듈: {', '.join(builder.modules.keys())}")
    else:
        builder.build_all()


if __name__ == "__main__":
    main()

"""
Usage: python build_gui.py {module_name} 
    eg) 
        specific build: python build_gui.py guidance
        all build:      python build_gui.py
"""
