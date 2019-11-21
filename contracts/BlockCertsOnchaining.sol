pragma solidity >0.5.0;

contract BlockCertsOnchaining {
	struct Batch {
		uint256 _merkleRootHash;
		bool _revoked;
	}
	struct Cert {
		bool _revoked;
	}

	address internal owner;
	// key: hash, value: Batch/Cert
	mapping(uint256 => Batch) public batches;
	mapping(uint256 => Cert) public revokedCerts;

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

	function issueBatch(uint256 _merkleRootHash) public onlyOwner {
		batches[_merkleRootHash] = Batch(_merkleRootHash, false);
	}

	function revokeBatch(uint256 _merkleRootHash) public onlyOwner {
		batches[_merkleRootHash]._revoked = true;
	}

	function revokeCert(uint256 _certHash) public onlyOwner {
		revokedCerts[_certHash]._revoked = true;
	}
}
