pragma solidity >0.5.0;

contract BlockCertsOnchaining {
	struct Hash {
		bool _revoked;
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
		hashes[_hash] = Hash(false);
	}

	function revoke_hash(uint256 _hash) public only_owner {
		hashes[_hash]._revoked = true;
	}
}
