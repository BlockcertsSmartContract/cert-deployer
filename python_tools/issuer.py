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
        print("could not issue cert with merkleRootHash " + str(merkleRootHash) + ". No permission?")
    # except ValidationError:
        # print("wrong arguments")

def getCertCount():
    certCount = issuer.functions.certCount().call()
    # print("number of certs issued so far " + str(certCount))
    return certCount

def getCertByIndex(index):
    try:
        return issuer.functions.certs(index).call()
    except:
        print("Could not get certificate by index: " + str(index) + ". Correct data type?")

# print("available functions: ", issuer.all_functions())

# issueCert(123)
# issueCert(111)

# change current wallet
# c.set_w3_wallet(1)
# won't work, as onlyOwner modifier is set
# issueCert(666)

# for i in range(0,getCertCount()):
    # print(getCertByIndex(i))



# issuer.functions.revokedCerts(1).call()

issuer.functions.issueCert(12, [5, 3]).transact()
print(getCertByIndex(12))
issuer.functions.revokeCert(12).transact()
print(getCertByIndex(12))


