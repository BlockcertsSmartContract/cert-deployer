#! /usr/bin/python

from connections import ContractConnection

# always accesses last deployed contract instance
c = ContractConnection('http://localhost:8545','../build/contracts/BlockCertsOnchaining.json')
issuer = c.get_contract_object()

# wrap function calls
def issueCert(merkleRootHash):
    try:
        issuer.functions.issueCert(merkleRootHash).transact()
        print("issued cert with merkleRootHash " + str(merkleRootHash))
    except ValueError:
        print("could not issue cert with merkleRootHash " + str(merkleRootHash))
    # except ValidationError:
        # print("wrong arguments")

def printCertCount():
    certCount = issuer.functions.certCount().call()
    print("number of certs issued so far " + str(certCount))

# print("available functions: ", issuer.all_functions())

issueCert(123)
issueCert(111)

printCertCount()

# change current wallet
c.set_w3_wallet(1)

# won't work, as onlyOwner modifier is set
issueCert(666)


a = issuer.functions.certs(1).call()
print(a)
