from setuptools import find_packages, setup

setup(
    name="morlingue",
    version="0.0.1",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "dash",
        "krakenex",
        "pandas",
        "plotly-express",
        "python-youtube",
        "web3",
        "cryptocompare",
    ],
    entry_points={
        "console_scripts": [
            "run_backend = morlingue.backend:main",
            "run_frontend = morlingue.frontend:main",
        ]
    },
)
