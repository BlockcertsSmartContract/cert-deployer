pragma solidity >0.5.0;

contract BlockCertsOnchaining {
	struct Hash {
		bool _revoked;
		bool _issued;
	}

	address internal owner;
	// key: hash, value: Batch/Cert
	mapping(uint256 => Hash) public hashes;

	modifier only_owner() {
		require(
			msg.sender == owner,
			"only contract owner can issue"
		);
		_;
	}

	constructor() public {
		owner = msg.sender;
	}

	function issue_hash(uint256 _hash) public only_owner {
		hashes[_hash]._revoked = false;
		hashes[_hash]._issued = true;
		
	}

	function revoke_hash(uint256 _hash) public only_owner {
		hashes[_hash]._revoked = true;
	}
}
