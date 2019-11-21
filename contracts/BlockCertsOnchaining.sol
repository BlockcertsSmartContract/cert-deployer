pragma solidity >0.5.0;

contract BlockCertsOnchaining {
	address internal owner;

	modifier onlyOwner() {
		require(
		    msg.sender == owner,
		    "only contract owner can issue"
		    );
		_;
	}
	
	constructor() public {
		owner = msg.sender;
	}
	
	mapping(uint256 => Certificate) public certs;
	
	struct Certificate {
		uint256 _merkleRootHash;
		bool _revoked;
	}

    // todo: check for permission
	function revokeCert(uint256 _merkleRootHash) public onlyOwner {
	    certs[_merkleRootHash]._revoked = true;
	}
	
	function issueCert(uint256 _merkleRootHash) public onlyOwner {
		certs[_merkleRootHash] = Certificate(_merkleRootHash, false);
	}
}
