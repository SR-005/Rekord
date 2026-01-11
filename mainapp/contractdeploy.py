from solcx import compile_standard, install_solc
import json
import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()
install_solc("0.8.17")

#-----------------------------------------------------------------COMPILING------------------------------------------------------------------

# Load Solidity file
with open("mainapp/contracts/simplenft.sol", "r") as f:
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
                "@openzeppelin/=mainapp/node_modules/@openzeppelin/"
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

with open("mainapp/contracts/compiled.json", "w") as file:
    json.dump(compiledsol, file, indent=2)

print("Compiled successfully!")

#fetching bytecode from the compiled Smart Contract
bytecode=compiledsol["contracts"]["contracts/simplenft.sol"]["SimpleNFT"]["evm"]["bytecode"]["object"]

#get abi from the compiled Smart Contract
abi=compiledsol["contracts"]["contracts/simplenft.sol"]["SimpleNFT"]["abi"]

#connecting to Ganache Blockchain
w3 = Web3(Web3.HTTPProvider(os.getenv("POLYGON_RPC")))

if not w3.is_connected():
    raise Exception("Not connected to Polygon")
else:
    print("Connected to Polygon Amoy")
    
chainid=80002

#-----------------------------------------------------------------DEPLOYMENT------------------------------------------------------------------

SimpleNFT=w3.eth.contract(abi=abi,bytecode=bytecode)
print("Contract Created")

MYADDRESS=Web3.to_checksum_address(os.getenv("METAMASK_ADDRESS"))
SECRETCODE=os.getenv("METAMASK_KEY")

nonce=w3.eth.get_transaction_count(MYADDRESS)

def contractdeployment():
    transaction=SimpleNFT.constructor().build_transaction({
        "from": MYADDRESS,
        "nonce": nonce,
        "gas": 1_000_000,
        "maxFeePerGas": w3.to_wei("60", "gwei"),
        "maxPriorityFeePerGas": w3.to_wei("30", "gwei"),
        "chainId": 80002
    })

    signedtransaction=w3.eth.account.sign_transaction(transaction, SECRETCODE)
    transactionhash=w3.eth.send_raw_transaction(signedtransaction.raw_transaction)
    receipt=w3.eth.wait_for_transaction_receipt(transactionhash)
    return transactionhash

'''contractaddress=contractdeployment()'''
contractaddress="0xaDA38E7b6b1e486Fb88fCf3346f7D26db51b5f0b" 

print("Contract Deployed on Polygon: ",contractaddress)
#-------------------------------------------------------------------TEST RUN----------------------------------------------------------------------
