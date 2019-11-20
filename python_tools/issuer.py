#! /usr/bin/python

from connections import ContractConnection

c = ContractConnection('http://localhost:8545','../build/contracts/BlockCertsOnchaining.json')
issuer = c.create_contract_object()

# print("available functions: ", issuer.all_functions())

c.set_w3_wallet(1)

issuer.functions.issueCert(666).transact()
print(issuer.functions.certCount().call())
print(issuer.functions.testVal().call())
