#! /usr/bin/python

from connections import ContractConnection

# always accesses last deployed contract instance
c = ContractConnection('http://localhost:8545','../build/contracts/BlockCertsOnchaining.json')
issuer = c.create_contract_object()

# print("available functions: ", issuer.all_functions())
print("# of certs issued so far")
print(issuer.functions.certCount().call())

print("issuing cert with hash 666")
issuer.functions.issueCert(666).transact()

print("# of certs issued so far")
print(issuer.functions.certCount().call())

c.set_w3_wallet(1)

print("trying to issue cert with hash 666")
try:
    issuer.functions.issueCert(666).transact()
except:
    print("only owner")

print("# of certs issued so far")
print(issuer.functions.certCount().call())

# print("test value (hardcoded)")
# print(issuer.functions.testVal().call())
