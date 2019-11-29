class Certificate:
    def __init__(self, merkleRootHash, certHash, contract_obj):
        self.contract_obj = contract_obj
        self.merkleRootHash = MRH(merkleRootHash, contract_obj)
        self.certHash = Hash(certHash, contract_obj)

    def issue(self):
        self.merkleRootHash.issue()

    def getBatchStatus(self):
        return self.merkleRootHash.getStatus()

    def getCertStatus(self):
        return self.certHash.getStatus()

    def revokeCert(self):
        self.certHash.revoke()

    def revokeBatch(self):
        self.merkleRootHash.revoke()

    def isCertValid(self, verbose=True):
        batchStatus = self.getBatchStatus()
        certStatus = self.getCertStatus()

        valid = False
        if batchStatus is False and certStatus is False:
            valid = True

        if verbose:
            print("> batch with merkleRootHash: " + str(self.merkleRootHash.hashVal) + " is revoked: "
                  + str(batchStatus))
            print("> cert with certHash " + str(self.certHash.hashVal) + " from batch "
                  + str(self.merkleRootHash.hashVal) + " is revoked: " + str(certStatus))
            print("> cert is valid: " + str(valid))

        return valid


class Hash:
    def __init__(self, hashVal, contract_obj):
        self.contract_obj = contract_obj
        self.hashVal = hashVal

    def revoke(self):
        self.contract_obj.functions.revokeHash(self.hashVal).transact()
        try:
            self.contract_obj.functions.revokeHash(self.hashVal).transact()
        except ValueError:
            print("could not revoke batch or cert with hash " + str(self.hashVal) + ". No permission?")

    def getStatus(self):
        return self.contract_obj.functions.hashes(self.hashVal).call()


class MRH(Hash):
    def issue(self):
        try:
            self.contract_obj.functions.issueHash(self.hashVal).transact()
        except ValueError:
            print("could not issue batch with merkleRootHash " + str(self.hashVal) + ". No permission?")
