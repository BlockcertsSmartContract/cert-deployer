pragma solidity >0.5.0;

contract BlockCertsOnchaining {
	//uint256 public certCount = 0;
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
		bool _revoked;
	}

    // todo: check for permission
	function revokeCert(uint256 _merkleRootHash) public {
	    certs[_merkleRootHash]._revoked = true;
	}
	
	function issueCert(uint256 _merkleRootHash) public onlyOwner {
		certs[_merkleRootHash] = Certificate(_merkleRootHash, false);
	}
}
