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
	
	modifier revocationPermission (Certificate memory cert) {
		// require(msg.sender exists in cert._revokers);
		/* require(
		    // closer to real life:
		    // msg.sender == cert.revokers[0],
		    5 == cert._revokers[0],
		    "revocation requires permission"
		    ); */
		_;
	}
	
	constructor() public {
		owner = msg.sender;
	}
	
	mapping(uint256 => Certificate) public certs;
	
	struct Certificate {
		uint256 _merkleRootHash;
		bool _revoked;
		// address[] _revokers;
		uint256[] _revokers;
	}

    // todo: check for permission
	function revokeCert(
	    uint256 _merkleRootHash
	    )
	    public revocationPermission(certs[_merkleRootHash])
	    {
	    certs[_merkleRootHash]._revoked = true;
	}
	
	function issueCert(uint256 _merkleRootHash, uint256[] memory _revokers) public onlyOwner {
		certs[_merkleRootHash] = Certificate(_merkleRootHash, false, _revokers);
	}
}
