"""
Cold Wallet Pinger — мониторинг активности "спящих" (cold) кошельков Ethereum.

Позволяет отслеживать долгосрочные кошельки, у которых давно не было исходящих транзакций,
и пинговать их через время, чтобы увидеть, "проснулись" ли они.

Полезно для мониторинга китов, early-инвесторов, забытых multisig'ов.
"""

import requests
import argparse
from datetime import datetime, timedelta


ETHERSCAN_API_URL = "https://api.etherscan.io/api"


def get_transactions(address, api_key):
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "apikey": api_key
    }
    response = requests.get(ETHERSCAN_API_URL, params=params)
    result = response.json()
    return result.get("result", [])


def check_cold_wallet(transactions, threshold_days=180):
    for tx in transactions:
        if tx["isError"] == "0" and tx["from"].lower() == address.lower():
            timestamp = int(tx["timeStamp"])
            last_active = datetime.utcfromtimestamp(timestamp)
            delta = datetime.utcnow() - last_active
            return {
                "last_active": last_active.strftime("%Y-%m-%d"),
                "days_since": delta.days,
                "status": "cold" if delta.days > threshold_days else "active"
            }
    return {
        "last_active": "never",
        "days_since": "∞",
        "status": "cold"
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cold Wallet Pinger — отслеживание активности холодных кошельков.")
    parser.add_argument("address", help="Ethereum-адрес")
    parser.add_argument("api_key", help="API-ключ от Etherscan")
    parser.add_argument("--threshold", type=int, default=180, help="Порог (в днях) бездействия для статуса cold")
    args = parser.parse_args()

    address = args.address
    api_key = args.api_key

    print(f"[•] Пингуем {address}...")

    txs = get_transactions(address, api_key)
    info = check_cold_wallet(txs, threshold_days=args.threshold)

    print("\n[✓] Последняя исходящая активность:")
    print(f"    Дата: {info['last_active']}")
    print(f"    Прошло дней: {info['days_since']}")
    print(f"    Статус: {'❄️ COLD' if info['status'] == 'cold' else '🔥 ACTIVE'}")
