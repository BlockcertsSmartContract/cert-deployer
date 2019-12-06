# Based on: https://web3py.readthedocs.io/en/stable/contracts.html

import argparse
import json

import onchaining_tools.config as config
import onchaining_tools.path_tools as tools
from onchaining_tools.connections import MakeW3
from solc import compile_standard

parser = argparse.ArgumentParser()


def compile_contract():
    w3_factory = MakeW3()
    w3 = w3_factory.get_w3_obj()
    acct = w3_factory.get_w3_wallet()

    with open(tools.get_contract_path()) as source_file:
        source_raw = source_file.read()

    with open(tools.get_compile_data_path()) as opt_file:
        raw_opt = opt_file.read()
        opt = json.loads(raw_opt)

    opt["sources"]["BlockCertsOnchaining.sol"]["content"] = source_raw
    compiled_sol = compile_standard(opt)
    bytecode = compiled_sol[
        'contracts']['BlockCertsOnchaining.sol']['BlockCertsOnchaining']['evm']['bytecode']['object']
    abi = json.loads(compiled_sol[
        'contracts']['BlockCertsOnchaining.sol']['BlockCertsOnchaining']['metadata'])['output']['abi']

    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    current_chain = config.config["current_chain"]
    acct_addr = config.config["wallets"][current_chain]["pubkey"]

    construct_txn = contract.constructor().buildTransaction({
        # 'from': acct_addr,
        'nonce': w3.eth.getTransactionCount(acct_addr),
        'gasPrice': w3.toWei('50', 'gwei'),
        'gas': 1000000
    })

    signed = acct.sign_transaction(construct_txn)
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    contr_address = tx_receipt.contractAddress
    data = {'abi': abi, 'address': contr_address}

    with open(tools.get_config_data_path(), "w+") as outfile:
        json.dump(data, outfile)

    print("deployed contract with address: " + str(contr_address))


if __name__ == '__main__':
    # args: deploy local or remote
    parser.add_argument("provider", help="supported providers are ropsten and ganache", type=str)
    arguments = parser.parse_args()
    if arguments.provider == "ropsten":
        try:
            config.config["current_chain"] = "ropsten"
            compile_contract()
        except ValueError:
            print("Something went wrong you should check your config.py")
    elif arguments.provider == "ganache":
        try:
            config.config["current_chain"] = "ganache"
            compile_contract()
        except ValueError:
            print("Something went wrong you should check your config.py")
    else:
        print("Please choose ropsten or ganache as provider")
