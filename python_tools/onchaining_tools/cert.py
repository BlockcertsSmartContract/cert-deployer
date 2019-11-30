class Certificate:
    def __init__(self, merkle_root_hash, cert_hash, contract_obj):
        self.contract_obj = contract_obj
        self.merkle_root_hash = MRH(merkle_root_hash, contract_obj)
        self.cert_hash = Hash(cert_hash, contract_obj)

    def issue(self) -> None:
        self.merkle_root_hash.issue()

    def get_batch_status(self) -> bool:
        return self.merkle_root_hash.get_status()

    def get_cert_status(self) -> bool:
        return self.cert_hash.get_status()

    def revoke_cert(self) -> None:
        self.cert_hash.revoke()

    def revoke_batch(self) -> None:
        self.merkle_root_hash.revoke()

    def is_cert_valid(self, verbose=True) -> bool:
        batch_status = self.get_batch_status()
        cert_status = self.get_cert_status()

        valid = False
        if batch_status is False and cert_status is False:
            valid = True

        if verbose:
            print("> batch with merkleRootHash: " + str(self.merkle_root_hash.hash_val) + " is revoked: "
                  + str(batch_status))
            print("> cert with cert_hash " + str(self.cert_hash.hash_val) + " from batch "
                  + str(self.merkle_root_hash.hash_val) + " is revoked: " + str(cert_status))
            print("> cert is valid: " + str(valid))

        return valid


class Hash:
    def __init__(self, hash_val, contract_obj) -> None:
        self.contract_obj = contract_obj
        self.hash_val = hash_val

    def revoke(self) -> None:
        try:
            self.contract_obj.functions.revokeHash(self.hash_val).transact()
        except ValueError:
            print("could not revoke batch or cert with hash " + str(self.hash_val) + ". No permission?")

    def get_status(self) -> bool:
        return self.contract_obj.functions.hashes(self.hash_val).call()


class MRH(Hash):
    def issue(self) -> None:
        try:
            self.contract_obj.functions.issueHash(self.hash_val).transact()
        except ValueError:
            print("could not issue batch with merkle_root_hash " + str(self.hash_val) + ". No permission?")
