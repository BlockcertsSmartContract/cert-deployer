import argparse
import json
from json import JSONDecodeError

import content_hash
import ipfshttpclient
import onchaining_tools.config as config
import onchaining_tools.path_tools as tools
from ens import ENS
from onchaining_tools.connections import ContractConnection, MakeW3

parser = argparse.ArgumentParser()
try:
    sc = ContractConnection("blockcertsonchaining")
except (KeyError, JSONDecodeError):
    print("Init your contr info first with deploy.py or issuer.py --init")


def get_contr_info_from_ens(address="blockcerts.eth"):
    client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
    try:
        ens_domain = str(address)
        ens_resolver = ContractConnection("ropsten_ens_resolver")

        w3 = MakeW3().get_w3_obj()
        ns = ENS.fromWeb3(w3)
        node = ns.namehash(ens_domain)

        contr_info = ""
        if client is not None:
            content = (ens_resolver.functions.call("contenthash", node)).hex()
            content = content_hash.decode(content)
            contr_info = str(client.cat(content))[2:-1]
        print(contr_info)
        with open(tools.get_contr_info_path(), "w+") as f:
            json.dump(json.loads(contr_info), f)
    except Exception:
        print("couldnt init contract info")
    client.close()


def issue(hash_val):
    '''Issues a certificate on the blockchain'''
    print("> following hash gets issued: " + str(hash_val))
    sc.functions.transact("issue_hash", hash_val)
    print("> successfully issued " + str(hash_val) + " on " + config.config["current_chain"])


def revoke(hash_val):
    '''Revokes a certficate by putting the certificate hash into smart contract revocation list'''
    print("> following hash gets revoked : " + str(hash_val))
    sc.functions.transact("revoke_hash", hash_val)
    print("> successfully revoked " + str(hash_val) + " on " + config.config["current_chain"])


def get_latest_contract():
    w3_factory = MakeW3()
    w3 = w3_factory.get_w3_obj()
    account = w3_factory.get_w3_wallet()
    ns = ENS.fromWeb3(w3, "0x112234455C3a32FD11230C42E7Bccd4A84e02010")

    name = ns.name(account.address)
    address = ns.address(name)
    print(address)


def verify(hash):
    '''Checks if the smart contract was issued and if it is on the revocation list'''
    cert_status = sc.functions.call("hashes", hash)

    valid = False
    if hash is False:
        valid = True

    print("> hash: " + str(hash) + " is revoked: "
          + str(cert_status))
    if valid:
        print("> hash is valid on " + config.config["current_chain"])
    else:
        print("> hash is not valid on " + config.config["current_chain"])


if __name__ == '__main__':
    '''Handles arguments and calls out respective functions'''
    parser.add_argument("hash", nargs='?', default=0, help="cert hash", type=int)
    parser.add_argument("-init", "--init", help="init contract info", action="store_true")
    parser.add_argument("-r", "--revoke", help="revoke hash", action="store_true")
    parser.add_argument("-i", "--issue", help="issue hash", action="store_true")
    parser.add_argument("-v", "--verify", help="verify cert", action="store_true")
    parser.add_argument("-c", "--contract", help="get info about most recently deployed contract", action="store_true")
    arguments = parser.parse_args()
    if arguments.init:
        get_contr_info_from_ens()
    elif arguments.issue:
        issue(arguments.hash)
    elif arguments.revoke:
        revoke(arguments.hash)
    elif arguments.verify:
        verify(arguments.hash)
    elif arguments.contract:
        get_latest_contract()
