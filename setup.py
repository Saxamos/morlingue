from setuptools import find_packages, setup

setup(
    name="morlingue",
    version="0.0.1",
    packages=find_packages(exclude=["tests"]),
    install_requires=[],
    entry_points={"console_scripts": [f"run = morlingue.main:main"]},
)
