from setuptools import find_packages, setup

setup(
    name="morlingue",
    version="0.0.1",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "streamlit",
        "krakenex",
        "pandas",
        "plotly-express",
        "schedule",
        "google-api-python-client",
        "google-auth-oauthlib",
        "google-auth-httplib2"
    ],
    entry_points={"console_scripts": ["run_backend = morlingue.backend"]},
)
