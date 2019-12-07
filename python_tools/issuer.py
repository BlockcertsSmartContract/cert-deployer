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

    ns = ENS.fromWeb3(w3, sc.get_contract_info()["blockcertsonchaining"]["address"])

    name = ns.name(str(config.config["wallets"][config.config["current_chain"]]["pubkey"]))
    address = ns.address(name)
    print(address)


def verify(merkle_root_hash, cert_hash):
    batch_status = sc.functions.call("hashes", merkle_root_hash)
    cert_status = sc.functions.call("hashes", cert_hash)

    valid = False
    if batch_status is False and cert_status is False:
        valid = True

    print("> batch with merkleRootHash: " + str(merkle_root_hash) + " is revoked: "
          + str(batch_status))
    print("> cert with certHash " + str(cert_hash) + " from batch "
          + str(merkle_root_hash) + " is revoked: " + str(cert_status))
    if valid:
        print("> cert is valid on " + config.config["current_chain"])
    else:
        print("> cert is not valid on " + config.config["current_chain"])


if __name__ == '__main__':
    parser.add_argument("cert_hash", help="cert or batch hash", type=int)
    parser.add_argument("batch_hash", help="batch hash", type=int)
    parser.add_argument("-rb", "--revokeBatch", help="revoke batch hash", action="store_true")
    parser.add_argument("-rc", "--revokeCert", help="revoke cert hash", action="store_true")
    parser.add_argument("-i", "--issue", help="revoke cert or batch hash", action="store_true")
    parser.add_argument("-v", "--verify", help="revoke cert or batch hash", action="store_true")
    parser.add_argument("-c", "--contract", help="get info about most recently deployed contract", action="store_true")
    arguments = parser.parse_args()
    if arguments.issue:
        issue(arguments.cert_hash)
    elif arguments.revokeCert:
        revoke(arguments.cert_hash)
    elif arguments.revokeBatch:
        revoke(arguments.batch_hash)
    elif arguments.verify:
        verify(arguments.batch_hash, arguments.cert_hash)
    elif arguments.contract:
        get_latest_contract()
