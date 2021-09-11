# Morlingue

This app displays assets evolution.

To run it locally, launch the following commands:
```
virtualenv -p python3 venv
source init.env
pip install -e .
run_backend
run_frontend
```
To run it remotely, do the same installation but ssh first:
```
ssh -i "morlingue.pem" <USER>@<MORLINGUE_IP>
cd morlingue
git pull
source init.env
pip install -e .
nohup run_backend &
nohup run_frontend &
nohup streamlit run bff/frontend.py &
```
To monitor your running app:
```
ps aux | grep streamlit
kill -9 26354
```

## TODO

- integrate eth metamask
- integrate uniswap pool
- integrate gold
- cache + refacto https://dash.plotly.com/sharing-data-between-callbacks
- integrate all asset that were in streamlit
- parametrize sliding window size
- automated CI and deployment travis
- ML model for forecasting