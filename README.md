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
- Automated attendance validation for virtual events using session duration analysis
- Backend-paid gas (users never pay gas)
- Dynamic NFT image generation
- IPFS-hosted images and metadata
- Physical and virtual event support
- Organization-based attendance tracking

---

## Attendance Verification (Virtual Events)

For virtual events, Rekord includes a server-side attendance verification system to ensure badges are issued only to genuine participants.
Organizers upload session data in CSV format containing participant join times, leave times, and session duration details. The backend processes this data to:

-Normalize and parse session timestamps
-Calculate total event duration
-Compute individual participant presence duration
-Apply a minimum attendance threshold (default: 75%)
-Automatically classify participants as Present or Absent

Only participants who meet the required presence criteria are marked eligible and receive claim links. This verification step is fully automated and runs before any badge minting occurs, preventing manual errors and fraudulent claims.

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
- Pillow (dynamic NFT image processing)
- Pandas & NumPy (attendance data parsing and verification)
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
