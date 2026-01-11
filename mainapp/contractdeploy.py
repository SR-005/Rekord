from solcx import compile_standard, install_solc
import json
import os
from dotenv import load_dotenv
from web3 import Web3

install_solc("0.8.17")

#-----------------------------------------------------------------COMPILING------------------------------------------------------------------

# Load Solidity file
with open("contracts/simplenft.sol", "r") as f:
    source = f.read()

compiledsol = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            # IMPORTANT: Use the REAL VIRTUAL FILE PATH
            "contracts/simplenft.sol": {"content": source}
        },
        "settings": {
            "remappings": [
                "@openzeppelin/=node_modules/@openzeppelin/"
            ],
            "outputSelection": {
                "*": {
                    "*": ["abi", "evm.bytecode"]
                }
            }
        }
    },
    solc_version="0.8.20"
)

with open("contracts/compiled.json", "w") as file:
    json.dump(compiledsol, file, indent=2)

print("Compiled successfully!")

#fetching bytecode from the compiled Smart Contract
bytecode=compiledsol["contracts"]["contracts/simplenft.sol"]["SimpleNFT"]["evm"]["bytecode"]["object"]

#get abi from the compiled Smart Contract
abi=compiledsol["contracts"]["contracts/simplenft.sol"]["SimpleNFT"]["abi"]

#connecting to Ganache Blockchain
w3=Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chainid=1337

#-----------------------------------------------------------------DEPLOYMENT------------------------------------------------------------------

SimpleNFT=w3.eth.contract(abi=abi,bytecode=bytecode)
print("Contract Created")

load_dotenv()
MYADDRESS = Web3.to_checksum_address(os.getenv("MYADDRESS"))
SECRETCODE = os.getenv("SECRETKEY")

nonce=w3.eth.get_transaction_count(MYADDRESS)

tx_hash = SimpleNFT.constructor().transact({
    "from": MYADDRESS,
    "gas": 3_000_000,
    "gasPrice": w3.to_wei("20", "gwei")
})

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Contract Deployed")

#-------------------------------------------------------------------TEST RUN----------------------------------------------------------------------
