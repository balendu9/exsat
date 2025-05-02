import os
import time
import requests
from dotenv import load_dotenv
from web3 import Web3
import json

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)
wallet = account.address
with open("abi.json", "r") as abi_file:
    CONTRACT_ABI = json.load(abi_file)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

EPOCH_DURATION = 120
PRICE_API = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
last_submitted_price = None

def fetch_price():
    try:
        response = requests.get(PRICE_API)
        return int(response.json()["bitcoin"]["usd"])
    except Exception as e:
        print(f"[ERROR] Fetching price: {e}")
        return None

def should_submit(price):
    global last_submitted_price
    if last_submitted_price is None or abs(price - last_submitted_price) > 1:
        last_submitted_price = price
        return True
    return False

def is_registered_oracle():
    try:
        return contract.functions.registeredOracles(wallet).call()
    except Exception as e:
        print(f"[ERROR] Checking registration: {e}")
        return False

def get_minimum_stake():
    try:
        return contract.functions.minimumStake().call()
    except Exception as e:
        print(f"[ERROR] Getting minimum stake: {e}")
        return w3.to_wei(0.01, 'ether')  # Fallback

def register_as_oracle():
    try:
        stake = get_minimum_stake()
        nonce = w3.eth.get_transaction_count(wallet)
        txn = contract.functions.registerOracle().build_transaction({
            'from': wallet,
            'value': stake,
            'nonce': nonce,
            'gas': 300000,
            'gasPrice': w3.to_wei('20', 'gwei')
        })
        signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"[✅] Registered as oracle. TX: {tx_hash.hex()}")
        w3.eth.wait_for_transaction_receipt(tx_hash)
        return True
    except Exception as e:
        print(f"[ERROR] Registration failed: {e}")
        return False

def submit_price(price):
    try:
        nonce = w3.eth.get_transaction_count(wallet)
        txn = contract.functions.submitPrice(price).build_transaction({
            'from': wallet,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': w3.to_wei('20', 'gwei')
        })
        signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"[📤] Submitted price: ${price} | TX: {tx_hash.hex()}")
    except Exception as e:
        print(f"[ERROR] Submitting price: {e}")

def main():
    print(f"[🔐] Wallet: {wallet}")
    if not is_registered_oracle():
        print("[🛠] Oracle not registered. Registering...")
        if not register_as_oracle():
            print("[❌] Could not register. Exiting.")
            return
    else:
        print("[✅] Oracle already registered.")

    print("[🔄] Starting oracle node...")
    while True:
        price = fetch_price()
        if price and should_submit(price):
            submit_price(price)
        else:
            print("[ℹ️] Skipping submission.")
        time.sleep(EPOCH_DURATION)

if __name__ == "__main__":
    main()
