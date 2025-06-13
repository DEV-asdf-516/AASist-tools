from pathlib import Path
from setuptools import setup, find_packages


def load_requirements(filename="requirements.txt"):
    path = Path(__file__).resolve().parent / filename
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]


setup(
    name="aasist",
    version="0.0.1",
    python_requires=">=3.11",
    packages=find_packages(),
    package_data={
        "": [
            "**/*.py",
            "config/*",
            "**/*.ico",
            "requirements.txt",
        ]
    },
    include_package_data=True,
    py_modules=["build_gui"],
    install_requires=load_requirements(),
    entry_points={"console_scripts": ["aasist-build = build_gui:main"]},
)
