class Certificate:
    def __init__(self, merkle_root_hash, certHash, contract_obj):
        self.contract_obj = contract_obj
        self.merkle_root_hash = MRH(merkle_root_hash, contract_obj)
        self.certHash = Hash(certHash, contract_obj)

    def issue(self):
        self.merkle_root_hash.issue()

    def get_batch_status(self):
        return self.merkle_root_hash.get_status()

    def get_cert_status(self):
        return self.certHash.get_status()

    def revoke_cert(self):
        self.certHash.revoke()

    def revoke_batch(self):
        self.merkle_root_hash.revoke()

    def is_cert_valid(self, verbose=True):
        batch_status = self.get_batch_status()
        cert_status = self.get_cert_status()

        valid = False
        if batch_status is False and cert_status is False:
            valid = True

        if verbose:
            print("> batch with merkleRootHash: " + str(self.merkle_root_hash.hash_val) + " is revoked: "
                  + str(batch_status))
            print("> cert with certHash " + str(self.certHash.hash_val) + " from batch "
                  + str(self.merkle_root_hash.hash_val) + " is revoked: " + str(cert_status))
            print("> cert is valid: " + str(valid))

        return valid


class Hash:
    def __init__(self, hash_val, contract_obj):
        self.contract_obj = contract_obj
        self.hash_val = hash_val

    def revoke(self):
        self.contract_obj.functions.revokeHash(self.hash_val).transact()
        try:
            self.contract_obj.functions.revokeHash(self.hash_val).transact()
        except ValueError:
            print("could not revoke batch or cert with hash " + str(self.hash_val) + ". No permission?")

    def get_status(self):
        return self.contract_obj.functions.hashes(self.hash_val).call()


class MRH(Hash):
    def issue(self):
        try:
            self.contract_obj.functions.issueHash(self.hash_val).transact()
        except ValueError:
            print("could not issue batch with merkleRootHash " + str(self.hash_val) + ". No permission?")
