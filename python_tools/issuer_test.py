import os
import unittest

from onchaining_tools.cert import Certificate
from onchaining_tools.connections import TruffleContract


def get_root_dir(x):
    root_dir = os.path.abspath(__file__)
    for _ in range(x):
        root_dir = os.path.dirname(root_dir)
    return root_dir


# always accesses last deployed contract instance
contract_conn = TruffleContract('http://localhost:8545', get_root_dir(2) + '/build/contracts/BlockCertsOnchaining.json')
contract_obj = contract_conn.get_contract_object()


class issuerTest(unittest.TestCase):

    def test_whenIssueCert_thenCertIsValidIsTrue(self):
        c1 = Certificate(100, 50, contract_obj)
        c1.issue()
        self.assertTrue(c1.is_cert_valid())

    def test_whenRevokeCert_thenCertIsValidIsFalse(self):
        c2 = Certificate(70, 90, contract_obj)
        c2.issue()
        c2.revoke_cert()
        self.assertFalse(c2.is_cert_valid())

    def test_whenRevokeBatch_thenCertIsValidIsFalse(self):
        c3 = Certificate(705, 905, contract_obj)
        c3.issue()
        c3.revoke_batch()
        self.assertFalse(c3.is_cert_valid())


if __name__ == '__main__':
    unittest.main()
