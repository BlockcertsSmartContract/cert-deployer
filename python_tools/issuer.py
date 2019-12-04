#! /usr/bin/python

import random
import sys
from onchaining_tools.connections import ContractConnection


def issue(merkle_root_hash=random.randint(100, 999)):
    '''calls out issuing fuction'''
    sc.functions.issue(merkle_root_hash)


def revoke(hash_val):
    '''calls out revokation function'''
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


sc = ContractConnection()

if __name__ == '__main__':
    arguments = len(sys.argv) - 1
    position = 1

    while arguments >= position:
        if sys.argv[position] == "--issue":
            try:
                issue(int(sys.argv[position + 1]))
            except IndexError:
                print("Error missing arguments for issuing (--issue [int]), issuing some random cert")
                issue()

        if sys.argv[position] == "--revoke":
            try:
                revoke(int(sys.argv[position + 1]))
            except IndexError:
                print("Error missing arguments for revocation (--revokeCert [int])")

        if sys.argv[position] == "--revokeBatch":
            try:
                revoke(int(sys.argv[position + 1]))
            except IndexError:
                print("Error missing arguments for revocation (--revokeBatch [int])")

        if sys.argv[position] == "--verify":
            try:
                verify(int(sys.argv[position + 1]), int(sys.argv[position + 2]))
            except IndexError:
                print("Error missing arguments for verifying (--verify [merkle_root_hash] [cert_hash])")

        position = position + 1
