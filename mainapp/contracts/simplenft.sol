// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract SimpleNFT is ERC721URIStorage, Ownable {

    uint256 public tokenCounter;

    // wallet => orgId => badge count
    mapping(address => mapping(uint256 => uint256)) public orgBadgeCount;

    constructor() ERC721("Rekord Badge", "RKB") {}

    function mintBadge(
        address to,
        uint256 orgId,
        string memory tokenURI
    ) external onlyOwner returns (uint256) {

        uint256 tokenId = tokenCounter;
        tokenCounter++;

        _safeMint(to, tokenId);
        _setTokenURI(tokenId, tokenURI);

        orgBadgeCount[to][orgId] += 1;

        return tokenId;
    }
}
