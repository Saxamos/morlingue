# Morlingue

This app displays assets evolution.

To run it locally, launch the following commands:
```
make setup_env
source init.env
run_backend
run_frontend
```
To run it remotely, do the same installation but ssh first:
```
ssh ubuntu@18.224.181.98
cd morlingue
git pull
source init.env
make run_prod
```
To monitor your running app:
```
ps aux | grep python
kill 26354
```
To back up locally the database:
```
scp ubuntu@18.224.181.98:/home/ubuntu/morlingue/pythonsqlite.db pythonsqlite.db
```

## TODO

- integrate uniswap pool
- integrate gold
- cache + refacto https://dash.plotly.com/sharing-data-between-callbacks
- integrate all asset that were in streamlit
- parametrize sliding window size
- automated CI and deployment travis
- ML model for forecasting