# Rekord

Rekord is a blockchain-based proof-of-attendance platform that enables organizations to issue **soul-bound NFT badges** to event participants. These badges act as permanent, non-transferable credentials that verify participation on-chain.

The system supports both **physical and virtual events**, with all minting gas fees handled by the backend to ensure a seamless user experience.

---

## Overview

Rekord allows organizations to create events and distribute unique claim links to participants. When a participant claims a badge:

1. A customized NFT image is generated dynamically
2. Image and metadata are uploaded to IPFS
3. A soul-bound ERC-721 NFT is minted directly to the participant’s wallet

Once minted, the badge cannot be transferred, sold, or approved.

---

## Key Features

- Soul-bound ERC-721 NFTs (non-transferable)
- Backend-paid gas (users never pay gas)
- Dynamic NFT image generation
- IPFS-hosted images and metadata
- Physical and virtual event support
- Organization-based attendance tracking

---

## Event & Badge Model

### Event Types

- **Physical Events**  
  In-person events where claim links are distributed via QR codes or email.

- **Virtual Events**  
  Online events where participants receive claim links digitally.

### Prestige and Loyalty Levels

Each event is created with a prestige level that affects badge design and significance:

- Standard  
- Signature  
- Flagship  

Loyalty is calculated at claim time based on a participant’s previous attendance with the same organization.  
Higher loyalty levels unlock additional visual elements within the badge.

---

## Soul-Bound NFT Design

Rekord badges are implemented as soul-bound ERC-721 tokens.

- Transfers are disabled at the smart contract level
- Token approvals are blocked
- Only minting from the zero address is allowed

Even if a wallet UI exposes a “Send” button, all transfer attempts revert on-chain.

---

## Technology Stack

### Frontend
- HTML, CSS, Bootstrap
- Vanilla JavaScript
- Ethers.js

### Backend
- Python
- Django
- Pillow (image processing)
- Web3.py
- Pinata IPFS API

### Blockchain
- Solidity
- OpenZeppelin Contracts
- Polygon (Amoy Testnet)

---


## Security Model

- Backend wallet signs and submits transactions
- No user private keys are ever handled by the server
- Metadata and images are immutable once pinned
- Minting restricted to contract owner

---

## License

MIT License
