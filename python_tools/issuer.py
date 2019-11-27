#! /usr/bin/python
from connections import ContractConnection
from compiler import compiling

local = true #need to have user entering bool if ganache or ropsten

issuer = compiling.compiler(local)

# always accesses last deployed contract instance
#c = ContractConnection('http://localhost:8545','/Users/florianweiss/Desktop/PAS_Git/BlockCertsOnchainingEth/build/contracts/BlockCertsOnchaining.json')
#issuer = c.get_contract_object()

# wrap function calls
def issueCert(merkleRootHash):
    try:
        issuer.functions.issueCert(merkleRootHash).transact()
        print("issued cert with merkleRootHash " + str(merkleRootHash))
    except ValueError:
        print("could not issue cert with merkleRootHash " + str(merkleRootHash) + ". No permission?")
    # except ValidationError:
        # print("wrong arguments")

def revokeCert(merkleRootHash):
    try:
        issuer.functions.revokeCert(merkleRootHash).transact()
        print("issued cert with merkleRootHash " + str(merkleRootHash))
    except ValueError:
        print("could not revoke cert with merkleRootHash " + str(merkleRootHash) + ". No permission?")

def getCertByMRH(index):
    """get certificate by merkle root hash"""
    try:
        return issuer.functions.certs(index).call()
    except:
        print("Could not get certificate by index: " + str(index) + ". Correct data type?")

issueCert(666)

issueCert(12)
print(getCertByMRH(12))
try:
    issuer.functions.revokeCert(12).transact()
except:
    print("couldn't revoke")
print(getCertByMRH(12))


