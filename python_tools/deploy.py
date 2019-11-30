# Based on: https://web3py.readthedocs.io/en/stable/contracts.html

import json

import onchaining_tools.path_tools as tools
from onchaining_tools.connections import MakeW3
from solc import compile_standard


def compile_contract(w3):
    with open(tools.get_contract_path()) as source_file:
        source_raw = source_file.read()

    with open(tools.get_compile_data_path()) as opt_file:
        raw_opt = opt_file.read()
        opt = json.loads(raw_opt)

    opt["sources"]["BlockCertsOnchaining.sol"]["content"] = source_raw

    compiled_sol = compile_standard(opt)

    bytecode = compiled_sol['contracts']['BlockCertsOnchaining.sol']['BlockCertsOnchaining']['evm']['bytecode'][
        'object']
    abi = \
        json.loads(compiled_sol['contracts']['BlockCertsOnchaining.sol']['BlockCertsOnchaining']['metadata'])['output'][
            'abi']

    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    tx_hash = contract.constructor().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    address = tx_receipt.contractAddress
    blockcerts_onchaining = w3.eth.contract(address=address, abi=abi)

    data = {'abi': abi, 'address': address}

    with open(tools.get_config_data_path(), "w+") as outfile:
        json.dump(data, outfile)

    return blockcerts_onchaining


def deploy(url):
    w3 = MakeW3(url).get_w3_obj()
    compile_contract(w3)


if __name__ == '__main__':
    # args: deploy local or remote
    deploy(tools.get_host())
