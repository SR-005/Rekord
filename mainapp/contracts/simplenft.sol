// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

//Mint Directly to the Function Caller
//Mint Directly to the Function Caller
/*contract SimpleNFT is ERC721URIStorage, Ownable
{
    uint public tokencounter;
    constructor () public ERC721 ("Badge1","NFTBadges")
    {
        tokencounter=0;         //count of total tokens minted
    }

    function CreateCollectible(string memory tokenuri) public returns (uint)
    {
        
        uint newtokenid=tokencounter;
        _safeMint(msg.sender, newtokenid);
        _setTokenURI(newtokenid, tokenuri);
        tokencounter=tokencounter+1; 
        return newtokenid;
    }
}*/

//Minted by backend to Desired User
contract SimpleNFT is ERC721URIStorage, Ownable
{
    uint public tokencounter;
    constructor () public ERC721 ("Badge1","NFTBadges")
    {
        tokencounter=0;         //count of total tokens minted
    }

    mapping(uint256 => string) public badgeLevel;
    function CreateCollectible(address to, string memory tokenuri, string memory level) public onlyOwner returns (uint)
    {
        
        uint newtokenid=tokencounter;
        _safeMint(to, newtokenid);
        _setTokenURI(newtokenid, tokenuri);
        badgeLevel[newtokenid] = level;         //to associate value of the badge to the badge id
        tokencounter=tokencounter+1; 
        return newtokenid;
    }
}