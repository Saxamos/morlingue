import logging
import os
import sqlite3
import time
from typing import Tuple

import krakenex
from cryptocompare import cryptocompare
from web3 import Web3

from morlingue import HOUR, ROOT_PATH

logging.getLogger().setLevel(logging.INFO)


def _request_data(kraken: krakenex.API, web3: Web3) -> Tuple[float, float]:

    ### TODO: request uniswap
    token_address = "0xfcb910d871d7e94f5a566b7b32fb2b19583c09d7"
    token_address_2 = "0x0d4a11d5eeaac28ec3f61d100daf4d40471f1852"
    abi = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function",
        },
        {
            "constant": True,
            "inputs": [],
            "name": "totalSupply",
            "outputs": [{"name": "", "type": "uint256"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function",
        },
    ]
    token = web3.eth.contract(address=Web3.toChecksumAddress(token_address), abi=abi)
    token_balance = token.functions.balanceOf(os.environ["METAMASK_ACCOUNT"]).call()
    token_total_supply = token.functions.totalSupply().call()
    ### TODO: convert to eur => https://etherscan.io/address/0xe07441ffb81ba73990c059463e7b253b3093f866
    # https://docs.uniswap.org/protocol/V2/reference/smart-contracts/pair#price0cumulativelast
    # https://v2.info.uniswap.org/pair/0xfcb910d871d7e94f5a566b7b32fb2b19583c09d7
    # https://etherscan.io/token/0xfcb910d871d7e94f5a566b7b32fb2b19583c09d7?a=0xe07441ffb81ba73990c059463e7b253b3093f866
    ### TODO: request uniswap

    kraken_total = kraken.query_private("TradeBalance", data={"asset": "ZEUR"})[
        "result"
    ]["eb"]
    metamask_balance = web3.eth.getBalance(os.environ["METAMASK_ACCOUNT"])
    eth_value = cryptocompare.get_price("ETH")["ETH"]["EUR"]
    metamask_total = float(web3.fromWei(metamask_balance, "ether")) * eth_value

    logging.info("Request: success")

    return kraken_total, metamask_total


def _persist_in_db(
    connection: sqlite3.Connection, kraken_total: float, metamask_total: float
) -> None:
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    cursor = connection.cursor()

    create_assets_table = """CREATE TABLE IF NOT EXISTS 
    assets (id INTEGER PRIMARY KEY,date TIME,kraken_total FLOAT,metamask_total FLOAT);"""
    cursor.execute(create_assets_table)

    insert_asset = (
        """INSERT INTO assets (date,kraken_total,metamask_total) VALUES (?,?,?);"""
    )
    cursor.execute(insert_asset, (current_time, kraken_total, metamask_total))
    connection.commit()


def main() -> None:

    kraken_api = krakenex.API(
        key=os.environ["KRAKEN_KEY"], secret=os.environ["KRAKEN_SECRET"]
    )
    db_connection = sqlite3.connect((ROOT_PATH.parent / "pythonsqlite.db").as_posix())
    infura_url = f"https://mainnet.infura.io/v3/{os.environ['INFURA_ID']}"
    web3 = Web3(Web3.HTTPProvider(infura_url))

    while True:

        try:
            kraken_total, metamask_total = _request_data(kraken_api, web3)
            _persist_in_db(db_connection, kraken_total, metamask_total)

        except Exception as e:
            logging.warning(f"Request: failed: {e}")

        time.sleep(HOUR)
