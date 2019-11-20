pragma solidity >0.5.0;

contract BlockCertsOnchaining {
    uint256 public certCount = 0;

    address internal owner;

    constructor() public {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    
    mapping(uint => Certificate) public certs;
    
    struct Certificate {
        uint256 _merkleRootHash;
        address _issuer;
    }
    
    function issueCert(uint256 _merkleRootHash) public onlyOwner {
        // check if msg.sender is allowed to issue
        certs[certCount] = Certificate(_merkleRootHash, msg.sender);
        certCount += 1;
    }
}
