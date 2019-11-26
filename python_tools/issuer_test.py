import unittest
from connections import ContractConnection
from cert import Certificate

# always accesses last deployed contract instance
contract_conn = ContractConnection('http://localhost:8545', '../build/contracts/BlockCertsOnchaining.json')
contract_obj = contract_conn.get_contract_object()

class issuerTest(unittest.TestCase):

    def test_whenIssueCert_thenCertIsValidIsTrue(self):
        c1 = Certificate(100, 50, contract_obj)
        c1.issue()
        self.assertTrue(c1.isCertValid())

    def test_whenRevokeCert_thenCertIsValidIsFalse(self):
        c2 = Certificate(70, 90, contract_obj)
        c2.issue()
        c2.revokeCert()
        self.assertFalse(c2.isCertValid())

    def test_whenRevokeBatch_thenCertIsValidIsFalse(self):
        c3 = Certificate(705, 905, contract_obj)
        c3.issue()
        c3.revokeBatch()
        self.assertFalse(c3.isCertValid())

if __name__ == '__main__':
    unittest.main()