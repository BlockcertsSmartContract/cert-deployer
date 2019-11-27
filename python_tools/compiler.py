#Based on: https://web3py.readthedocs.io/en/stable/contracts.html

import json
from web3 import Web3
from solc import compile_standard

class compiling:
	def compiler():
		#if(local):
		nodeurl = "http://localhost:8545"
		#else:
			#nodeurl = "https://ropsten.infura.io/hqRzEqFKv6IsjRxfVUWH" 

		compiled_sol = compile_standard({
			"language": "Solidity",
			"sources": {
				"BlockCerts_Onchaining.sol": {
				 "content": '''
					pragma solidity >0.5.0;

					contract BlockCerts_Onchaining {
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

				   '''
				}
			},
			"settings": {
				"outputSelection": {
					"*": {
						"*": [
							"metadata", "evm.bytecode", "evm.bytecode.sourceMap"
						]
					}
				}
			}
		})

		w3 = Web3(Web3.HTTPProvider(nodeurl))
		#if(local):
		w3.eth.defaultAccount = w3.eth.accounts[0]
		#else:
			#w3.eth.defaultAccount = "0xB4d9313EE835b3d3eE7759826e1F3C3Ac23dFaf3"		

		bytecode = compiled_sol['contracts']['BlockCerts_Onchaining.sol']['BlockCerts_Onchaining']['evm']['bytecode']['object']
		abi = json.loads(compiled_sol['contracts']['BlockCerts_Onchaining.sol']['BlockCerts_Onchaining']['metadata'])['output']['abi']
		
		BlockCertsOnchaining = w3.eth.contract(abi=abi, bytecode=bytecode)		
		
		#NEED TO SOLVE ROPSTEN UNLOCKING 
		#w3.eth.personal.unlockAccount("0xB4d9313EE835b3d3eE7759826e1F3C3Ac23dFaf3", "50F3DCA79D43C17C0B58B88BAF57F0D91212F7CA6A9EDC4781C96A5E99FB573D", 1000)
		#w3.eth.account.signTransaction(BlockCertsOnchaining, '50F3DCA79D43C17C0B58B88BAF57F0D91212F7CA6A9EDC4781C96A5E99FB573D')
		
		tx_hash = BlockCertsOnchaining.constructor().transact()
		tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
		
		print(tx_receipt)

		return BlockCertsOnchaining