from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="gdstarter",
    description="A simple CLI tool for creating Godot projects.",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["inquirer", "requests"],
    extras_require={
        "dev": [
            "twine",
        ]
    },
    entry_points={
        "console_scripts": [
            "gdstarter = gdstarter.main:main",
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)
