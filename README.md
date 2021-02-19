# Morlingue

This app displays assets evolution.

To run it locally, launch the following commands:
```
virtualenv -p python3 venv
source init.env
pip install -e .
nohup run_backend &
streamlit run morlingue/frontend.py 
```

To run it remotely, do the same but ssh first:
```
ssh -i "morlingue.pem" ubuntu@3.21.240.92
```

### TODO

- autoreload when new data are coming
- add etoro
- add bourso
