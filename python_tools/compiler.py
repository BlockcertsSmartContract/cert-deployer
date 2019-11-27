#Based on: https://web3py.readthedocs.io/en/stable/contracts.html

import json
from web3 import Web3
from solc import compile_standard

class compiling:
	def compiler():
		#if(local):
			#nodeurl = "http://localhost:8545"
		#else:
		nodeurl = "https://ropsten.infura.io/hqRzEqFKv6IsjRxfVUWH" 

		compiled_sol = compile_standard({
			"language": "Solidity",
			"sources": {
				"BlockCerts_Onchaining.sol": {
				 "content": '''
					pragma solidity >0.5.0;

					contract BlockCerts_Onchaining{
						string value = "Lappen";

						smartcontract public sc;
						
						modifier onlyIssuer(){
							require(msg.sender == sc.issuerID);
							_;
						}
						
						struct smartcontract{
							address issuerID;
							bool revoked;
						}
						
						constructor() public{ //pass recipient address via function call
							sc.issuerID = msg.sender; //msg.sender is the one deploying this SC					        
							sc.revoked = false;
						}

						//GETTER SETTER
						function getIssuerID() public view returns(address){
							return sc.issuerID;
						}
						
						function getValue() public view returns(string memory){
							return value;
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
		#	w3.eth.defaultAccount = w3.eth.accounts[0]
		#else:
		w3.eth.defaultAccount = "0xB4d9313EE835b3d3eE7759826e1F3C3Ac23dFaf3"		

		bytecode = compiled_sol['contracts']['BlockCerts_Onchaining.sol']['BlockCerts_Onchaining']['evm']['bytecode']['object']
		abi = json.loads(compiled_sol['contracts']['BlockCerts_Onchaining.sol']['BlockCerts_Onchaining']['metadata'])['output']['abi']
		
		BlockCertsOnchaining = w3.eth.contract(abi=abi, bytecode=bytecode)		
		
		w3.eth.personal.unlockAccount("0xB4d9313EE835b3d3eE7759826e1F3C3Ac23dFaf3", "50F3DCA79D43C17C0B58B88BAF57F0D91212F7CA6A9EDC4781C96A5E99FB573D", 1000)
		#w3.eth.account.signTransaction(BlockCertsOnchaining, '50F3DCA79D43C17C0B58B88BAF57F0D91212F7CA6A9EDC4781C96A5E99FB573D')
		
		tx_hash = BlockCertsOnchaining.constructor().transact()
		tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
		print(tx_receipt)

		return BlockCertsOnchaining