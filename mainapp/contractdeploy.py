from solcx import compile_standard, install_solc
import json
import os
from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

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
            "mainapp/contracts/simplenft.sol": {"content": source}
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
bytecode=compiledsol["contracts"]["mainapp/contracts/simplenft.sol"]["SimpleNFT"]["evm"]["bytecode"]["object"]

#get abi from the compiled Smart Contract
abi=compiledsol["contracts"]["mainapp/contracts/simplenft.sol"]["SimpleNFT"]["abi"]

#connecting to Ganache Blockchain
w3 = Web3(Web3.HTTPProvider(os.getenv("POLYGON_RPC")))
w3.middleware_onion.inject(ExtraDataToPOAMiddleware(), layer=0)

if not w3.is_connected():
    raise Exception("Not connected to Polygon")
else:
    print("Connected to Polygon Amoy")
    
chainid=80002
print([f["name"] for f in abi if f["type"] == "function"])
#-----------------------------------------------------------------DEPLOYMENT------------------------------------------------------------------

SimpleNFT=w3.eth.contract(abi=abi,bytecode=bytecode)
print("Contract Created")

MYADDRESS=Web3.to_checksum_address(os.getenv("METAMASK_ADDRESS"))
SECRETCODE=os.getenv("METAMASK_KEY")

#un-comment to re deploy the contract
'''nonce=w3.eth.get_transaction_count(MYADDRESS)
transaction=SimpleNFT.constructor().build_transaction({
    "from": MYADDRESS,
    "nonce": nonce,
    "gas": 3_000_000,
    "maxFeePerGas": w3.to_wei("60", "gwei"),
    "maxPriorityFeePerGas": w3.to_wei("30", "gwei"),
    "chainId": 80002
})

signedtransaction=w3.eth.account.sign_transaction(transaction, SECRETCODE)
transactionhash=w3.eth.send_raw_transaction(signedtransaction.raw_transaction)
transactionreceipt=w3.eth.wait_for_transaction_receipt(transactionhash)
contractaddress=transactionreceipt.contractAddress'''

contractaddress="0x67839A1002036F8a7db0B0F3c17765c534cE6c4F"
print("Contract Address: ",contractaddress)
contractinstance=w3.eth.contract(address=contractaddress,abi=abi)
print("Contract Instacnce: ",contractinstance)


#get count of badges minted by particular organization
def getcount(walletaddress):
    code = w3.eth.get_code(contractaddress)
    print("Contract code length:", len(code))

    organizationid=1
    count=contractinstance.functions.orgBadgeCount(walletaddress,organizationid).call()
    print("Count: ",count)
    return count

#mint badges
def mintbadge(walletaddress,orgid,tokenuri):
    mint_nonce=w3.eth.get_transaction_count(MYADDRESS)
    mint_transaction=contractinstance.functions.mintBadge(walletaddress,orgid,tokenuri).build_transaction({
        "from": MYADDRESS,
        "nonce": mint_nonce,
        "gas": 3_000_000,
        "maxFeePerGas": w3.to_wei("60", "gwei"),
        "maxPriorityFeePerGas": w3.to_wei("30", "gwei"),
        "chainId": 80002
    })

    mint_signedtransaction=w3.eth.account.sign_transaction(mint_transaction, SECRETCODE)
    mint_transactionhash=w3.eth.send_raw_transaction(mint_signedtransaction.raw_transaction)
    mint_transactionreceipt=w3.eth.wait_for_transaction_receipt(mint_transactionhash)
    print("Reciept: ",mint_transactionreceipt.transactionHash.hex())

    return mint_transactionreceipt.transactionHash.hex()



if __name__ == "__main__":
    mintbadge(MYADDRESS,1,"ipfs://Qme9NMgqojmXvtkx39BM9pDxaHZ1NHxaYQM9eirP7ifW1w")
    #getcount("walletaddress")