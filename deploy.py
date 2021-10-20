import pdb
import os
import json
from web3 import Web3
from dotenv import load_dotenv
from solcx import compile_standard, install_solc


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    print(simple_storage_file)
# We add these two lines that we forgot from the video!
print("Installing...")
install_solc("0.6.0")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"][
    "SimpleStorage"]["evm"]["bytecode"]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
# pdb; pdb.set_trace()
w3 = Web3(Web3.HTTPProvider("https://kovan.infura.io/v3/a5b6a7d9d6fd4899a0390452946ea3ec"))
chain_id = 42
my_address = "0x2F2691D4395b9510Dc9747658C3f294AFB30d135"
private_key = os.getenv("PRIVATE_KEY")

# createthecontract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)


#Build a transaction
nonce = w3.eth.getTransactionCount(my_address)

transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address,"nonce": nonce}
)
#sign the address using a private key
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
#send the signed transaction
tx_hash = w3.eth.send_raw_transaction((signed_txn.rawTransaction))
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

print(simple_storage.functions.retrieve().call())
# create a transaction
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)
# sign a transaction
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
# wait for transaction to finish
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print(simple_storage.functions.retrieve().call())
