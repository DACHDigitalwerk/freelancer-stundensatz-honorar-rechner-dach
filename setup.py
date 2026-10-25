from setuptools import setup, find_packages

setup(
    name="stundensatz-dach",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "dach-stundensatz=stundensatz_dach.cli:main",
        ],
    },
)
