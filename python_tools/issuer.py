#! /usr/bin/python

from connections import ContractConnection

c = ContractConnection('http://localhost:8545','../build/contracts/BlockCertsOnchaining.json')
issuer = c.create_contract_object()


issuer.functions.issueCert(666).transact()
print(issuer.functions.certCount().call())
print(issuer.functions.testVal().call())
