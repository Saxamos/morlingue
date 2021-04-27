import os
import sqlite3
import time
from typing import Dict

import krakenex

from morlingue import ROOT_PATH

KRAKEN_KEY = os.environ["KRAKEN_KEY"]
KRAKEN_SECRET = os.environ["KRAKEN_SECRET"]
kraken = krakenex.API(key=KRAKEN_KEY, secret=KRAKEN_SECRET)
crypto_dict = kraken.query_private("Balance")["result"]

connection = sqlite3.connect((ROOT_PATH.parent / "pythonsqlite.db").as_posix())


def _insert_assets(
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


def _insert_crypto(
    connection: sqlite3.Connection, current_time: time, crypto: Dict[str, str]
) -> None:
    cursor = connection.cursor()
    create_crypto_table = (
        "CREATE TABLE IF NOT EXISTS crypto (date TIME,XXBT FLOAT,XETH FLOAT,XLTC FLOAT, XMANA FLOAT, BCH FLOAT)"
    )
    cursor.execute(create_crypto_table)
    insert_asset = "INSERT INTO crypto (date,XXBT,XETH,XLTC,XMANA,BCH) VALUES (?,?,?,?,?,?);"
    cursor.execute(insert_asset, (current_time, *tuple(crypto.values())))
    connection.commit()


def job(
    connection: sqlite3.Connection, kraken: krakenex.API, crypto_dict: Dict[str, str]
) -> None:
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    total = kraken.query_private("TradeBalance", data={"asset": "ZEUR"})["result"]["eb"]
    _insert_assets(connection, current_time, total)

    # crypto_eur = {"XXBT": 0, "XETH": 0, "XLTC": 0, "MANA": 0, "BCH": 0}
    # for crypto in crypto_eur.keys():
    #     pair = f"{crypto}ZEUR" if crypto != "MANA" else "MANAEUR"
    #     change = kraken.query_public("Ticker", data={"pair": pair})["result"][pair][
    #         "a"
    #     ][0]
    #     crypto_eur[crypto] = float(crypto_dict[crypto]) * float(change)
    #     time.sleep(1)
    # _insert_crypto(connection, current_time, crypto_eur)
    print("request")


while True:
    job(connection, kraken, crypto_dict.copy())
    time.sleep(600)
