import unittest

from onchaining_tools.connections import ContractConnection

sc = ContractConnection("blockcertsonchaining")


class issuerTest(unittest.TestCase):
    def test_whenIssueCert_thenCertIsValidIsTrue(self):
        cert_hash = 1000000

        sc.functions.transact("issue_hash", cert_hash)

        self.assertTrue(not sc.functions.call("hashes", cert_hash))

    def test_whenRevokeCert_thenCertIsValidIsFalse(self):
        cert_hash = 1000001

        sc.functions.transact("issue_hash", cert_hash)
        self.assertTrue(not sc.functions.call("hashes", cert_hash))

        sc.functions.transact("revoke_hash", cert_hash)
        self.assertTrue(sc.functions.call("hashes", cert_hash))


if __name__ == '__main__':
    unittest.main()
