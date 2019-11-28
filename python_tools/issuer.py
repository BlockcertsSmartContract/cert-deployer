from connections import TruffleContract
from cert import Certificate
from compiler import compile_contract
import random
import sys
import os

# always accesses last deployed contract instance
def get_root_dir():
    root_dir = os.path.abspath(__file__)
    for _ in range(2):
        root_dir = os.path.dirname(root_dir)
    return root_dir
  
absFilePath = get_root_dir() + '/build/contracts/BlockCertsOnchaining.json'
contract_conn = TruffleContract('http://localhost:8545', absFilePath )

contract_obj = contract_conn.get_contract_object()
# contract_obj = compile_contract(contract_conn.w3)
# print(contract_obj.accounts)


def issue(merkle_root_hash = random.randint(100, 999), cert_hash = random.randint(100, 999)):
    cert_mock = Certificate(merkle_root_hash, cert_hash, contract_obj)
    cert_mock.issue()
    cert_mock.isCertValid()

def revoke_cert(merkle_root_hash, cert_hash):
    cert_mock = Certificate(merkle_root_hash, cert_hash, contract_obj)
    cert_mock.revokeCert()
    cert_mock.isCertValid()

def revoke_batch(merkle_root_hash, cert_hash):
    cert_mock = Certificate(merkle_root_hash, cert_hash, contract_obj)
    cert_mock.revokeBatch()
    cert_mock.isCertValid()

if __name__ == '__main__':
    arguments = len(sys.argv) - 1
    position = 1
    while (arguments >= position):
        if (sys.argv[position] == "--issue"):
            try:
                issue(int(sys.argv[position+1]), int(sys.argv[position+2]))
            except:
                print("Error missing arguments for issueing (--issue int int), issueing some random cert")
                issue()
        if (sys.argv[position] == "--revokeCert"):
            try:
                revoke_cert(int(sys.argv[position+1]), int(sys.argv[position+2]))
            except:
                print("Error missing arguments for revocation (--revokeCert int int)")
        if (sys.argv[position] == "--revokeBatch"):
            try:
                revoke_cert(int(sys.argv[position+1]), int(sys.argv[position+2]))
            except:
                print("Error missing arguments for revocation (--revokeBatch int int)")
        position = position + 1
