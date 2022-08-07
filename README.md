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
ssh ec2-user@13.37.244.32
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

- transfert data from Joey
- setup aws instance
- finish add uniswap
- [add DNS](https://www.noip.com/)
- doc & migration script
- separate kraken from staking in second graph
- add boursorama
- integrate more assets (gold, loan, ...)
- automated CI and deployment travis
- ML model for forecasting