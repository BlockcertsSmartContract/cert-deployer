import unittest

import onchaining_tools.tools as tools
from onchaining_tools.cert import Certificate
from onchaining_tools.connections import TruffleContract

contract_conn = TruffleContract(tools.get_host(), tools.get_contract_as_json_path())
contract_obj = contract_conn.get_contract_object()


class issuerTest(unittest.TestCase):

    def test_whenIssueCert_thenCertIsValidIsTrue(self):
        cert_mock_1 = Certificate(100, 50, contract_obj)

        cert_mock_1.issue()

        self.assertTrue(cert_mock_1.is_cert_valid())

    def test_whenRevokeCert_thenCertIsValidIsFalse(self):
        cert_mock_2 = Certificate(70, 90, contract_obj)

        cert_mock_2.issue()
        cert_mock_2.revoke_cert()

        self.assertFalse(cert_mock_2.is_cert_valid())

    def test_whenRevokeBatch_thenCertIsValidIsFalse(self):
        cert_mock_3 = Certificate(705, 905, contract_obj)

        cert_mock_3.issue()
        cert_mock_3.revoke_batch()

        self.assertFalse(cert_mock_3.is_cert_valid())


if __name__ == '__main__':
    unittest.main()
