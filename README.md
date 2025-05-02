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

3. Create a `.env` file or just rename the .env.example to .env with provide your wallet private key(create a new wallet and fund it):


PRIVATE_KEY=YourWalletKey
RPC_URL=https://evm-tst3.exsat.network/
CONTRACT_ADDRESS=oraclecontract


-> .env.example already has correct data, just add your wallet private key

4. Run the oracle node:
python oracle_node.py
or 
python3 oracle_node.py