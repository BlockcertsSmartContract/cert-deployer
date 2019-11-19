#! /usr/bin/python

from web3 import Web3, HTTPProvider
import json

contract_info = ""
with open('../build/contracts/BlockCertsOnchaining.json') as file:
    data = file.read()
    contract_info = json.loads(data)

abi = contract_info["abi"]
address = contract_info["networks"]["5777"]["address"]
print(address)

# connecting to local ethereum node using ganache
w3 = Web3(HTTPProvider('http://localhost:8545'))
w3.eth.defaultAccount = w3.eth.accounts[0]

# print(w3.eth.getBlock("latest"))

certsc = w3.eth.contract(address=address,abi=abi)

certsc.functions.issueCert(666).transact()
print(certsc.functions.certCount().call())
print(certsc.functions.testVal().call())
