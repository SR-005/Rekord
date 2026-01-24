import requests
import os
from dotenv import load_dotenv

load_dotenv()

PINATA_API=os.getenv("PINATA_API")
PINATA_KEY=os.getenv("PINATA_KEY")
PINATA_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"

def upload(file_bytes,file):
    headers={"pinata_api_key": PINATA_API, "pinata_secret_api_key": PINATA_KEY}
    files={"file": (file, file_bytes)}

    response=requests.post(PINATA_URL,headers=headers,files=files)
    if response.status_code != 200:
        raise Exception(f"Pinata upload failed: {response.text}")

    ipfshash=response.json()["IpfsHash"]
    print("IPFS Hash: ",ipfshash)
    return ipfshash

def metadata(event,imageipfs):
    metadata = {
        "name": f"Rekord – {event.eventname}",
        "description": f"Proof of attendance for {event.eventname}",
        "image": f"ipfs://{imageipfs}",
        "attributes": [
            {"trait_type": "Event Type", "value": event.eventtype},
            {"trait_type": "City", "value": event.city},
            {"trait_type": "Date", "value": event.eventdate},
            {"trait_type": "Prestige", "value": event.eventprestige},
        ]
    }
    return ipfshash

if __name__ == "__main__":
    upload(0,0) 