import subprocess
import sys
import shutil
from pathlib import Path
from typing import Any
from tqdm import tqdm
import pkg_resources


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

        self.project_root: Path = Path.cwd()
        self.dist_path = self.project_root / "AASist Tools"
        self.build_path = self.project_root / "build"
        self.package_name = "aasist"
        self.package_folders = ["aasist"]
        self.package_files = ["requirements.txt"]
        self.modules = {
            "guidance": {
                "entry": "src/gui/aasist_guidance/main.py",
                "name": "AASist_Guidance",
                "icon": "icons/guidance.ico",
            },
            "test": {
                "entry": "src/gui/aasist_test/main.py",
                "name": "AASist_Test",
                "icon": "icons/test.ico",
            },
            "one": {
                "entry": "src/gui/aasist_one/main.py",
                "name": "AASist_One",
                # "icon": "icons/integration.ico",
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

    def extract_package_files(self):
        try:
            for folder in self.package_folders:
                if pkg_resources.resource_exists(self.package_name, folder):
                    target_dir = self.project_root / folder
                    target_dir.mkdir(exist_ok=True)
                    self._extract_folder(folder, target_dir)

            for file in self.package_files:
                if pkg_resources.resource_exists(self.package_name, file):
                    self._extract_file(file)

        except Exception as e:
            print(f"Error extracting package files: {e}")

    def _extract_file(self, file_name: str, target_path: Path = None):
        try:
            if not target_path:
                target_path = self.project_root / Path(file_name).name
            target_path.parent.mkdir(parents=True, exist_ok=True)
            file = pkg_resources.resource_string(self.package_name, file_name)
            with open(target_path, "wb") as f:
                f.write(file)
        except Exception as e:
            print(f"Error extracting file {file_name}: {e}")

    def _extract_folder(self, resource_path: str, target_dir: Path):
        try:
            if pkg_resources.resource_isdir(self.package_name, resource_path):
                resources = pkg_resources.resource_listdir(
                    self.package_name, resource_path
                )
                for r in resources:
                    r_path = f"{resource_path}/{r}"
                    target_path: Path = target_dir / r
                    if pkg_resources.resource_isdir(self.package_name, r_path):
                        target_path.mkdir(exist_ok=True)
                        self._extract_folder(r_path, target_dir=target_path)
                    else:
                        self._extract_file(r_path, target_path=target_path)
        except Exception as e:
            print(f"Error extracting folder {resource_path}: {e}")
            return

    def clean_build_folders(self):
        if self.build_path.exists():
            shutil.rmtree(self.build_path)
        for spec_file in self.project_root.glob("*.spec"):
            spec_file.unlink()

    def build_module(self, module_name, config: dict[str, Any]):
        pkg = pkg_resources.get_distribution(self.package_name)
        lib_path = Path(pkg.location) / self.package_name

        entry_path = lib_path / config["entry"]
        work_path = self.build_path / module_name
        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            f"--name={config['name']}",
            f"--distpath={self.dist_path}",
            f"--workpath={str(work_path)}",
            "--clean",
        ]

        if config.get("icon") and Path(config["icon"]).exists():
            cmd.extend(["--icon", lib_path / config["icon"]])

        cmd.extend(["--collect-all", self.package_name])

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

        cmd.append(entry_path)

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
        self.extract_package_files()
        self.dist_path.mkdir(exist_ok=True)
        for module_name, config in self.modules.items():
            self.build_module(module_name, config)
        self._list_exe_files()
        self.clean_build_folders()

    def _list_exe_files(self):
        for exe_file in self.dist_path.glob("*.exe"):
            size_mb = exe_file.stat().st_size / (1024 * 1024)
            print(f"  • {exe_file.name} ({size_mb:.1f} MB)")

    def _process_output(self, process: subprocess.Popen, module_name: str):
        module_name = f"{module_name:<16}"
        error_line: str = None

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
                    error_line = str(line).strip()
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

        if error_line:
            print(f"\033[91m{error_line}\033[0m")


def main():
    builder = GUIBuilder()

    if len(sys.argv) > 1:
        module_name = sys.argv[1]
        if module_name in builder.modules:
            builder.extract_package_files()
            builder.dist_path.mkdir(exist_ok=True)
            builder.build_module(module_name, builder.modules[module_name])
            builder.clean_build_folders()
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
