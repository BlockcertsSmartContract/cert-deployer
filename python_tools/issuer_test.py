import unittest

from onchaining_tools.connections import ContractConnection

sc = ContractConnection()


class issuerTest(unittest.TestCase):

    def test_whenIssueCert_thenCertIsValidIsTrue(self):
        cert_hash = 1000000

        sc.functions.issue(cert_hash)

        self.assertTrue(not sc.functions.get_status(cert_hash))

    def test_whenRevokeCert_thenCertIsValidIsFalse(self):
        cert_hash = 1000001

        sc.functions.issue(cert_hash)
        self.assertTrue(not sc.functions.get_status(cert_hash))

        sc.functions.revoke(cert_hash)
        self.assertTrue(sc.functions.get_status(cert_hash))

    if __name__ == '__main__':
        unittest.main()
