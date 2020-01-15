import argparse
import json
import logging
import os
import subprocess
import sys
import time
import uuid
from json import JSONDecodeError

import content_hash
import ipfshttpclient
import onchaining_tools.config as config
import onchaining_tools.path_tools as tools
from ens import ENS
from onchaining_tools.connections import ContractConnection, MakeW3

sessionid = uuid.uuid4()
logging.basicConfig(filename="onchainging.log", level=logging.INFO,
                    format='Session {}: %(asctime)s:%(message)s'.format(sessionid))
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

parser = argparse.ArgumentParser()
try:
    sc = ContractConnection("blockcertsonchaining")
except (KeyError, JSONDecodeError):
    logging.error("Init your contr info first with deploy.py or issuer.py --init")


def get_contr_info_from_ens(address="blockcerts.eth"):
    try:
        FNULL = open(os.devnull, 'w')
        subprocess.Popen(["ipfs", "daemon"], stdout=FNULL, stderr=subprocess.STDOUT, close_fds=True)
        FNULL.close()
        time.sleep(10)
        client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
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
        with open(tools.get_contr_info_path(), "w+") as f:
            json.dump(json.loads(contr_info), f)
        FNULL = open(os.devnull, 'w')
        subprocess.Popen(["ipfs", "shutdown"], stdout=FNULL, stderr=subprocess.STDOUT, close_fds=True)
        FNULL.close()
        client.close()
    except Exception:
        logging.error("couldnt init contract info")


def issue(hash_val):
    '''Issues a certificate on the blockchain'''
    logging.info("> following hash gets issued: {}".format(hash_val))
    sc.functions.transact("issue_hash", hash_val)
    logging.info("> successfully issued {} on {}".format(hash_val, config.config["current_chain"]))


def revoke(hash_val):
    '''Revokes a certficate by putting the certificate hash into smart contract revocation list'''
    logging.info("> following hash gets revoked : {}".format(hash_val))
    sc.functions.transact("revoke_hash {}".format(hash_val))
    logging.info("> successfully revoked {} on {}".format(hash_val, config.config["current_chain"]))


def get_latest_contract():
    w3_factory = MakeW3()
    w3 = w3_factory.get_w3_obj()
    account = w3_factory.get_w3_wallet()
    ns = ENS.fromWeb3(w3, "0x112234455C3a32FD11230C42E7Bccd4A84e02010")

    name = ns.name(account.address)
    address = ns.address(name)
    logging.info(address)


def verify(hash_val):
    '''Checks if the smart contract was issued and if it is on the revocation list'''
    cert_status = sc.functions.call("hashes", hash_val)

    if cert_status == 0:
        logging.info("> hash is not issued on {}".format(config.config["current_chain"]))
    elif cert_status == 1:
        logging.info("> hash is valid on {}".format(config.config["current_chain"]))
    elif cert_status == 2:
        logging.info("> hash is revoked on {}".format(config.config["current_chain"]))


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
