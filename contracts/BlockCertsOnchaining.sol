pragma solidity >0.5.0;

contract BlockCertsOnchaining {
	struct Hash {
		bool _revoked;
	}

	address internal owner;
	// key: hash, value: Batch/Cert
	mapping(uint256 => Hash) public hashes;

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

	function issueHash(uint256 _hash) public onlyOwner {
		hashes[_hash] = Hash(false);
	}

	function revokeHash(uint256 _hash) public onlyOwner {
		hashes[_hash]._revoked = true;
	}
}
