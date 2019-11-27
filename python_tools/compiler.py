#Based on: https://web3py.readthedocs.io/en/stable/contracts.html

import json
from web3 import Web3
from solc import compile_standard

class compiling:
	def compiler(local):
		if(local):
			nodeurl = "http://localhost:8545"
		else:
			nodeurl = "https://ropsten.infura.io/hqRzEqFKv6IsjRxfVUWH" 

		compiled_sol = compile_standard({
		    "language": "Solidity",
		    "sources": {
	        	"Greeter.sol": {
	             "content": '''
	                pragma solidity >0.5.0;

					contract BlockCerts_Onchaining{
					    smartcontract public sc;
					    
					    modifier onlyIssuer(){
					        require(msg.sender == sc.issuerID);
					        _;
					    }
					    
					    struct smartcontract{
					        address issuerID;
					        bool revoked;
					    }
					    
					    constructor(address recipientaddress) public{ //pass recipient address via function call
					        sc.issuerID = msg.sender; //msg.sender is the one deploying this SC					        
					        sc.revoked = false;
					    }

					    //GETTER SETTER
					    function getRecipientID() public view returns(address){
					        return sc.recipientID;
					    }
					    
					    function getIssuerID() public view returns(address){
					        return sc.issuerID;
					    }
					    
					    //REVOCATION
					    function revoke() public onlyIssuer{ //have to make sure only the issuer revokes
					        sc.revoked = true;
					    }
					    
					    function getRevoked() public view returns(bool){
					        return sc.revoked;
					    }
					}
	               '''
	         }
	     },
	     "settings":
	         {
	             "outputSelection": {
	                 "*": {
	                     "*": [
	                         "metadata", "evm.bytecode"
	                         , "evm.bytecode.sourceMap"
	                     ]
	                 }
	             }
	         }
	 	})

		w3 = Web3(HTTPProvider(nodeurl))
		w3.eth.defaultAccount = w3.eth.accounts[0]
		bytecode = compiled_sol['contracts']['BlockCerts_Onchaining.sol']['BlockCerts_Onchaining']['evm']['bytecode']['object']
		abi = json.loads(compiled_sol['contracts']['BlockCerts_Onchaining.sol']['BlockCerts_Onchaining']['metadata'])['output']['abi']
		BlockCertsOnchaining = w3.eth.contract(abi=abi, bytecode=bytecode)
		tx_hash = BlockCertsOnchaining.constructor().transact()
		tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

		return BlockCertsOnchaining









