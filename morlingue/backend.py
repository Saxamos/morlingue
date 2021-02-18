import os
import sqlite3
import time
from pathlib import Path

import krakenex
import schedule

from morlingue import ROOT_PATH

KRAKEN_KEY = os.environ["KRAKEN_KEY"]
KRAKEN_SECRET = os.environ["KRAKEN_SECRET"]
kraken = krakenex.API(key=KRAKEN_KEY, secret=KRAKEN_SECRET)


def insert_in_db(kraken_value: float, db_path: Path = ROOT_PATH.parent / "pythonsqlite.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    create_table = "CREATE TABLE IF NOT EXISTS assets (id INTEGER PRIMARY KEY,kraken_total FLOAT,date TIME);"
    cursor.execute(create_table)

    insert_asset = "INSERT INTO assets (kraken_total,date) VALUES (?,?);"
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(insert_asset, (kraken_value, current_time))
    conn.commit()


def display_db(db_path: Path = ROOT_PATH.parent / "pythonsqlite.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * from assets")
    # data = cursor.fetchall()
    # print(data)


def job() -> None:
    balance = kraken.query_private("TradeBalance", data={"asset": "ZEUR"})
    total_euros = balance["result"]["eb"]
    insert_in_db(total_euros)
    print(f"Kraken: {total_euros}€")


schedule.every(5).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
