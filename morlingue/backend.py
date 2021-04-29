import os
import sqlite3
import time

import krakenex

from morlingue import ROOT_PATH, HOUR

KRAKEN_API = krakenex.API(
    key=os.environ["KRAKEN_KEY"], secret=os.environ["KRAKEN_SECRET"]
)
CRYPTO_DICT = KRAKEN_API.query_private("Balance")["result"]
DB_CONNECTION = sqlite3.connect((ROOT_PATH.parent / "pythonsqlite.db").as_posix())


def _insert_kraken(
    connection: sqlite3.Connection, current_time: time, kraken_total: float
) -> None:
    cursor = connection.cursor()
    create_assets_table = (
        "CREATE TABLE IF NOT EXISTS assets "
        "(id INTEGER PRIMARY KEY,kraken_total FLOAT,date TIME);"
    )
    cursor.execute(create_assets_table)
    insert_asset = "INSERT INTO assets (kraken_total,date) VALUES (?,?);"
    cursor.execute(insert_asset, (kraken_total, current_time))
    connection.commit()


def job(connection: sqlite3.Connection, kraken: krakenex.API) -> None:
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    total = kraken.query_private("TradeBalance", data={"asset": "ZEUR"})["result"]["eb"]
    _insert_kraken(connection, current_time, total)
    print("request")


while True:
    job(DB_CONNECTION, KRAKEN_API)
    time.sleep(HOUR)
