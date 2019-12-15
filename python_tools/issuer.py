import argparse

import onchaining_tools.config as config
from ens import ENS
from onchaining_tools.connections import ContractConnection, MakeW3

parser = argparse.ArgumentParser()
sc = ContractConnection("blockcertsonchaining")


def issue(hash_val):
    print("> following hash gets issued: " + str(hash_val))
    sc.functions.transact("issue_hash", hash_val)
    print("> successfully issued " + str(hash_val) + " on " + config.config["current_chain"])


def revoke(hash_val):
    print("> following hash gets revoked : " + str(hash_val))
    sc.functions.transact("revoke_hash", hash_val)
    print("> successfully revoked " + str(hash_val) + " on " + config.config["current_chain"])


def get_latest_contract():
    w3_factory = MakeW3()
    w3 = w3_factory.get_w3_obj()

    ns = ENS.fromWeb3(w3, "0x112234455C3a32FD11230C42E7Bccd4A84e02010")

    name = ns.name(str(config.config["wallets"][config.config["current_chain"]]["pubkey"]))
    address = ns.address(name)
    print(address)


def verify(hash):
    cert_status = sc.functions.call("hashes", hash)

    valid = False
    if cert_status == 0:
    print("> hash is not issued on " + config.config["current_chain"])

    elif cert_status == 1:
        valid = True
        print("> hash is valid on " + config.config["current_chain"])

    elif cert_status == 2:
        print("> hash is revoked on " + config.config["current_chain"])


if __name__ == '__main__':
    parser.add_argument("hash", nargs='?', default=0, help="cert hash", type=int)
    parser.add_argument("-r", "--revoke", help="revoke hash", action="store_true")
    parser.add_argument("-i", "--issue", help="issue hash", action="store_true")
    parser.add_argument("-v", "--verify", help="verify cert", action="store_true")
    parser.add_argument("-c", "--contract", help="get info about most recently deployed contract", action="store_true")
    arguments = parser.parse_args()
    if arguments.issue:
        issue(arguments.hash)
    elif arguments.revoke:
        revoke(arguments.hash)
    elif arguments.verify:
        verify(arguments.hash)
    elif arguments.contract:
        get_latest_contract()
