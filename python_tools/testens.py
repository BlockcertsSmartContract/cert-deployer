from web3 import Web3
import json
from solc import compile_standard

from ens import ENS

class testens:
	web3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/a70de76e3fd748cbb6dbb2ed49dda183"))
	ns = ENS.fromWeb3(web3, "0x112234455C3a32FD11230C42E7Bccd4A84e02010") #registry
	#"0xB4d9313EE835b3d3eE7759826e1F3C3Ac23dFaf3") #metamask

	eth_address = ns.address('blockcertstest.eth')
	print("Address is: " + str(eth_address))

	name = ns.name("0xB4d9313EE835b3d3eE7759826e1F3C3Ac23dFaf3")#'0x5133B52166efCBD0Bf3A442b66eCC49c8b747AA2')
	print("Name is: " + str(name))

	eth_owner = ns.owner('blockcertstest.eth')
	print("Owner is: " + eth_owner)

	# temp = ns.namehash("flo.test")
	# print("Namehash is: " + str(temp))

	# #code for calling functions directly form ropsten registry contract 
	# abi = [{"constant":true,"inputs":[{"name":"node","type":"bytes32"}],"name":"resolver","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"node","type":"bytes32"}],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"node","type":"bytes32"},{"name":"label","type":"bytes32"},{"name":"owner","type":"address"}],"name":"setSubnodeOwner","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"node","type":"bytes32"},{"name":"ttl","type":"uint64"}],"name":"setTTL","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"node","type":"bytes32"}],"name":"ttl","outputs":[{"name":"","type":"uint64"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"node","type":"bytes32"},{"name":"resolver","type":"address"}],"name":"setResolver","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"node","type":"bytes32"},{"name":"owner","type":"address"}],"name":"setOwner","outputs":[],"payable":false,"type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"node","type":"bytes32"},{"indexed":false,"name":"owner","type":"address"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"node","type":"bytes32"},{"indexed":true,"name":"label","type":"bytes32"},{"indexed":false,"name":"owner","type":"address"}],"name":"NewOwner","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"node","type":"bytes32"},{"indexed":false,"name":"resolver","type":"address"}],"name":"NewResolver","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"node","type":"bytes32"},{"indexed":false,"name":"ttl","type":"uint64"}],"name":"NewTTL","type":"event"}]
	# address = "0x112234455C3a32FD11230C42E7Bccd4A84e02010"
	# contract = web3.eth.contract(address=address, abi=abi)

	# print(contract.functions.resolver(temp).call())
	# print("Should be equals: 0x12299799a50340FB860D276805E78550cBaD3De3")
	
	# "privkey": "50f3dca79d43c17c0b58b88baf57f0d91212f7ca6a9edc4781c96a5e99fb573d"