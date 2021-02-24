# Morlingue

This app displays assets evolution.

To run it locally, launch the following commands:
```
virtualenv -p python3 venv
source init.env
pip install -e .
run_backend
streamlit run morlingue/frontend.py
```
To run it remotely, do the same installation but ssh first:
```
ssh -i "morlingue.pem" <USER>@<MORLINGUE_IP>
cd morlingue
git pull
source init.env
nohup run_backend &
nohup streamlit run morlingue/frontend.py &
```
To monitor your running app:
```
ps aux | grep streamlit
kill -9 26354
```

## TODO

- integrate value variation (gold)
- integrate value variation (eth metamask)
- intergrate dynamics assets with scrapper
- automated CI and deployment travis
- ML model for forecasting
- try dash frontend
- sort lines
- create kraken all values plot