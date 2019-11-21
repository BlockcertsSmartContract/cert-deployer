#! /usr/bin/python

from connections import ContractConnection
from cert import Certificate

# always accesses last deployed contract instance
contract_conn = ContractConnection('http://localhost:8545','../build/contracts/BlockCertsOnchaining.json')
contract_obj = contract_conn.get_contract_object()

c1 = Certificate(10, 11, contract_obj)

print("issue batch:")
c1.issueBatch()
c1.isCertValid()
print()
print("revoke Batch")
c1.revokeBatch()
c1.isCertValid()
print()
c1.revokeCert()
c1.isCertValid()
