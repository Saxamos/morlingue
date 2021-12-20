import logging
import os
import sqlite3
import time

import krakenex
from cryptocompare import cryptocompare
from web3 import Web3

from morlingue import HOUR, ROOT_PATH

logging.getLogger().setLevel(logging.INFO)


KRAKEN_API = krakenex.API(
    key=os.environ["KRAKEN_KEY"], secret=os.environ["KRAKEN_SECRET"]
)
CRYPTO_DICT = KRAKEN_API.query_private("Balance")["result"]
DB_CONNECTION = sqlite3.connect((ROOT_PATH.parent / "pythonsqlite.db").as_posix())

INFURA_URL = f"https://mainnet.infura.io/v3/{os.environ['INFURA_ID']}"
WEB3 = Web3(Web3.HTTPProvider(INFURA_URL))


def _insert_kraken(
    connection: sqlite3.Connection,
    current_time: str,
    kraken_total: float,
    metamask_total: float,
) -> None:
    cursor = connection.cursor()

    create_assets_table = """CREATE TABLE IF NOT EXISTS 
    assets (id INTEGER PRIMARY KEY,date TIME,kraken_total FLOAT,metamask_total FLOAT);"""
    cursor.execute(create_assets_table)

    insert_asset = (
        """INSERT INTO assets (date,kraken_total,metamask_total) VALUES (?,?,?);"""
    )
    cursor.execute(insert_asset, (current_time, kraken_total, metamask_total))
    connection.commit()


def job(connection: sqlite3.Connection, kraken: krakenex.API) -> None:
    try:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")

        kraken_total = kraken.query_private("TradeBalance", data={"asset": "ZEUR"})[
            "result"
        ]["eb"]

        metamask_balance = WEB3.eth.getBalance(os.environ["METAMASK_ACCOUNT"])
        eth_value = cryptocompare.get_price("ETH")["ETH"]["EUR"]
        metamask_total = float(WEB3.fromWei(metamask_balance, "ether")) * eth_value

        _insert_kraken(connection, current_time, kraken_total, metamask_total)
        logging.info("Request: success")
    except Exception as e:
        logging.warning(f"Request: failed: {e}")


def main() -> None:
    while True:
        job(DB_CONNECTION, KRAKEN_API)
        time.sleep(HOUR)
