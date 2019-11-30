#! /usr/bin/python

import random
import sys
import argparse
from connections import TruffleContract, SelfDeployedContract
from cert import Certificate


# contract_conn = TruffleContract('http://localhost:8545', '../build/contracts/BlockCertsOnchaining.json')
contract_conn = SelfDeployedContract('http://localhost:8545', '../data/contr_info.json')

contract_obj = contract_conn.get_contract_object()


def issue(merkle_root_hash=random.randint(100, 999), cert_hash=random.randint(100, 999)):
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
                print("Error missing arguments for issuing (--issue int int), issuing some random cert")
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
