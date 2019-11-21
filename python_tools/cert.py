class Certificate:
    def __init__(self, merkleRootHash, certHash, contract_obj):
        self.merkleRootHash = merkleRootHash
        self.certHash = certHash
        self.contract_obj = contract_obj

    def issueBatch(self):
        try:
            self.contract_obj.functions.issueBatch(self.merkleRootHash).transact()
        except ValueError:
            print("could not issue batch with merkleRootHash " + str(self.merkleRootHash) + ". No permission?")

    def revokeBatch(self):
        try:
            self.contract_obj.functions.revokeBatch(self.merkleRootHash).transact()
        except ValueError:
            print("could not revoke batch with batch hash " + str(self.merkleRootHash) + ". No permission?")

    def revokeCert(self):
        try:
            self.contract_obj.functions.revokeCert(self.certHash).transact()
        except ValueError:
            print("could not revoke cert with cert hash " + str(self.certHash) + ". No permission?")

    def getCertInfo(self):
        try:
            return self.contract_obj.functions.revokedCerts(self.certHash).call()
        except:
            print("Could not get certificate by certHash: " + str(self.certHash) + ". Correct data type?")

    def getBatchInfo(self):
        try:
            return self.contract_obj.functions.batches(self.merkleRootHash).call()
        except:
            print("Could not get batch by batchHash: " + str(self.merkleRootHash) + ". Correct data type?")

    def isCertValid(self, verbose=True):
        batchInfo = self.getBatchInfo()
        certInfo = self.getCertInfo()
        valid = not (batchInfo[0] == 0 or batchInfo[1] == True or certInfo == True)
        
        if verbose:
            print("batch with batch merkleRootHash: " + str(batchInfo[0]) + " is revoked: " + str(batchInfo[1]))
            print("cert with certHash " + str(self.certHash) + " from batch " + str(batchInfo[0]) + " is revoked: " + str(certInfo))
            print("cert is valid: " + str(valid))


