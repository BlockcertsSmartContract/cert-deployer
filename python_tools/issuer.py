import random
import sys

import onchaining_tools.tools as tools
from onchaining_tools.cert import Certificate
from onchaining_tools.connections import TruffleContract

contract_conn = TruffleContract('http://localhost:8545', tools.get_contract_as_json_path())

contract_obj = contract_conn.get_contract_object()


def issue(merkle_root_hash=random.randint(100, 999), cert_hash=random.randint(100, 999)) -> None:
    cert_mock = Certificate(merkle_root_hash, cert_hash, contract_obj)
    cert_mock.issue()
    cert_mock.is_cert_valid()


def revoke_cert(merkle_root_hash, cert_hash) -> None:
    cert_mock = Certificate(merkle_root_hash, cert_hash, contract_obj)
    cert_mock.revoke_cert()
    cert_mock.is_cert_valid()


def revoke_batch(merkle_root_hash, cert_hash) -> None:
    cert_mock = Certificate(merkle_root_hash, cert_hash, contract_obj)
    cert_mock.revoke_batch()
    cert_mock.is_cert_valid()


if __name__ == '__main__':
    arguments = len(sys.argv) - 1
    position = 1
    while arguments >= position:
        if sys.argv[position] == "--issue":
            try:
                issue(int(sys.argv[position + 1]), int(sys.argv[position + 2]))
            except IndexError:
                print("Error missing arguments for issueing (--issue int int), issueing some random cert")
                issue()
        if sys.argv[position] == "--verifyCert":
            try:
                Certificate(int(sys.argv[position + 1]), int(sys.argv[position + 2]), contract_obj).is_cert_valid()
            except IndexError:
                print("Error missing arguments for verifying (--verifyCert int int)")
        if sys.argv[position] == "--revokeCert":
            try:
                revoke_cert(int(sys.argv[position + 1]), int(sys.argv[position + 2]))
            except IndexError:
                print("Error missing arguments for revocation (--revokeCert int int)")
        if sys.argv[position] == "--revokeBatch":
            try:
                revoke_cert(int(sys.argv[position + 1]), int(sys.argv[position + 2]))
            except IndexError:
                print("Error missing arguments for revocation (--revokeBatch int int)")
        position = position + 1
