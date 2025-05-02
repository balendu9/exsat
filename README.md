# 🧠 BTC Oracle Node

This is an off-chain node script that submits BTC prices to a decentralized oracle contract on Ethereum.

## ✅ Requirements

- Python 3.7+
- ETH wallet with gas
- Fund you wallet with btc testnet tokens: https://faucet.exsat.network/
## 🚀 Setup

1. Clone the repo
2. Install dependencies:

pip install -r requirements.txt

3. Create a `.env` file:


PRIVATE_KEY=YourWalletKey
RPC_URL=https://evm-tst3.exsat.network/
CONTRACT_ADDRESS=0xYourContract


4. Run the oracle node:
python oracle_node.py
or 
python3 oracle_node.py