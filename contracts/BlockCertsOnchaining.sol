pragma solidity >0.5.0;

contract BlockCertsOnchaining {
    uint256 public certCount = 0;
    uint public testVal = 12;
    
    mapping(uint => Certificate) public certs;
    
    struct Certificate {
        uint256 _merkleRootHash;
        address _issuer;
    }
    
    function issueCert(uint256 _merkleRootHash) public {
        // check if msg.sender is allowed to issue
        certs[certCount] = Certificate(_merkleRootHash, msg.sender);
        certCount += 1;
    }
}
