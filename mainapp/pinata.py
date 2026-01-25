import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

PINATAAPI=os.getenv("PINATA_API")
PINATAKEY=os.getenv("PINATA_KEY")
PINATAURL = "https://api.pinata.cloud/pinning/pinFileToIPFS"

#function to upload image to pinata
def upload(file_bytes,file):
    headers={"pinata_api_key": PINATAAPI, "pinata_secret_api_key": PINATAKEY}
    files={"file": (file, file_bytes)}

    response=requests.post(PINATAURL,headers=headers,files=files)
    if response.status_code != 200:
        raise Exception(f"Pinata upload failed: {response.text}")

    ipfshash=response.json()["IpfsHash"]
    print("IPFS Hash: ",ipfshash)
    return ipfshash


#function to upload metadata
def metadata(event,imagecid):
    #metadata format
    metadata = {
        "name": f"Rekord – {event.eventname}",
        "description": f"Proof of attendance for {event.eventname}",
        "image": f"ipfs://{imagecid}",
        "attributes": [
            {"trait_type": "Event Type", "value": event.eventtype},
            {"trait_type": "City", "value": event.city},
            {"trait_type": "Date", "value": event.eventdate},
            {"trait_type": "Prestige", "value": event.eventprestige},
        ]
    }
    metadatajson=json.dumps(metadata)

    #header of API Request
    headers = {
        "Content-Type": "application/json",
        "pinata_api_key": PINATAAPI,
        "pinata_secret_api_key": PINATAKEY,
    }

    response = requests.post(
        "https://api.pinata.cloud/pinning/pinJSONToIPFS",
        headers=headers,
        data=metadatajson
    )

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()["IpfsHash"]

if __name__ == "__main__":
    upload(0,0) 