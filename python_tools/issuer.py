#! /usr/bin/python

import argparse
import random

from onchaining_tools.connections import ContractConnection

parser = argparse.ArgumentParser()
sc = ContractConnection()


def issue(merkle_root_hash=random.randint(100, 999)):
    sc.functions.issue(merkle_root_hash)


def revoke(hash_val):
    sc.functions.revoke(hash_val)


def verify(merkle_root_hash, cert_hash):
    batch_status = sc.functions.get_status(merkle_root_hash)
    cert_status = sc.functions.get_status(cert_hash)

    valid = False
    if batch_status is False and cert_status is False:
        valid = True

    print("> batch with merkleRootHash: " + str(merkle_root_hash) + " is revoked: "
          + str(batch_status))
    print("> cert with certHash " + str(cert_hash) + " from batch "
          + str(merkle_root_hash) + " is revoked: " + str(cert_status))
    print("> cert is valid: " + str(valid))


if __name__ == '__main__':
    parser.add_argument("cert_hash", help="cert or batch hash", type=int)
    parser.add_argument("batch_hash", help="batch hash", type=int)
    parser.add_argument("-rb", "--revokeBatch", help="revoke batch hash", action="store_true")
    parser.add_argument("-rc", "--revokeCert", help="revoke cert hash", action="store_true")
    parser.add_argument("-i", "--issue", help="revoke cert or batch hash", action="store_true")
    parser.add_argument("-v", "--verify", help="revoke cert or batch hash", action="store_true")
    arguments = parser.parse_args()
    if arguments.issue:
        try:
            issue(arguments.cert_hash)
        except IndexError:
            print("Error missing arguments for issuing (--issue [int]), issuing some random cert")
            issue()
    elif arguments.revokeCert:
        try:
            revoke(arguments.cert_hash)
        except IndexError:
            print("Error missing arguments for revocation (--revokeCert [int])")
    elif arguments.revokeBatch:
        try:
            revoke(arguments.batch_hash)
        except IndexError:
            print("Error missing arguments for revocation (--revokeBatch [int])")
    if arguments.verify:
        try:
            verify(arguments.batch_hash, arguments.cert_hash)
        except IndexError:
            print("Error missing arguments for verifying (--verify [merkle_root_hash] [cert_hash])")
