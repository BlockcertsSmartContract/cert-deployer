#! /usr/bin/python

from connections import ContractConnection

# always accesses last deployed contract instance
c = ContractConnection('http://localhost:8545','../build/contracts/BlockCertsOnchaining.json')
issuer = c.get_contract_object()

# wrap function calls
def issueBatch(merkleRootHash):
    try:
        issuer.functions.issueBatch(merkleRootHash).transact()
    except ValueError:
        print("could not issue batch with merkleRootHash " + str(merkleRootHash) + ". No permission?")

def revokeBatch(batchHash):
    try:
        issuer.functions.revokeBatch(batchHash).transact()
    except ValueError:
        print("could not revoke batch with batch hash " + str(batchHash) + ". No permission?")

def revokeCert(certHash):
    try:
        issuer.functions.revokeCert(certHash).transact()
    except ValueError:
        print("could not revoke cert with cert hash " + str(certHash) + ". No permission?")

def getCertInfo(certHash):
    try:
        return issuer.functions.revokedCerts(certHash).call()
    except:
        print("Could not get certificate by certHash: " + str(certHash) + ". Correct data type?")

def getBatchInfo(batchHash):
    try:
        return issuer.functions.batches(batchHash).call()
    except:
        print("Could not get batchificate by batchHash: " + str(batchHash) + ". Correct data type?")

issueBatch(12)
print(getBatchInfo(12))
print(getBatchInfo(11))
revokeBatch(12)
print(getBatchInfo(12))
revokeBatch(12)
revokeCert(13)
print(getCertInfo(13))
