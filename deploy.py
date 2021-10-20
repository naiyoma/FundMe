import pdb
import json
from web3 import Web3
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
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0xAfEd3A49a7EA22155F38063b06A17C11Fe2251e3"
private_key = "0xa00e8effcd76964a452ba8c1acd6d70b374a95ce478127d379c10dee40e8012d"

# createthecontract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)


#Build a transaction
nonce = w3.eth.getTransactionCount(my_address)

transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address,"nonce": nonce}
)
#sign the address using a private key
pdb; pdb.set_trace()
