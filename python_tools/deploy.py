# Based on: https://web3py.readthedocs.io/en/stable/contracts.html

import json
from solc import compile_standard
from connections import MakeW3


def compile_contract(w3):
    source_raw = ""
    with open("../contracts/BlockCertsOnchaining.sol") as source_file:
        source_raw = source_file.read()

    opt = ""
    with open("../data/compile_opt.json") as opt_file:
        raw_opt = opt_file.read()
        opt = json.loads(raw_opt)

    opt["sources"]["BlockCertsOnchaining.sol"]["content"] = source_raw

    compiled_sol = compile_standard(opt)

    bytecode = compiled_sol['contracts']['BlockCertsOnchaining.sol']['BlockCertsOnchaining']['evm']['bytecode']['object']
    abi = json.loads(compiled_sol['contracts']['BlockCertsOnchaining.sol']['BlockCertsOnchaining']['metadata'])['output']['abi']

    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    tx_hash = contract.constructor().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    address = tx_receipt.contractAddress
    blockCertsOnchaining = w3.eth.contract(address=address, abi=abi)

    data = {}
    data['abi'] = abi
    data['address'] = address

    with open("../data/contr_info.json", "w+") as outfile:
        json.dump(data, outfile)

    return blockCertsOnchaining

def deploy(url):
    w3 = MakeW3(url).get_w3_obj()
    compile_contract(w3)


if __name__ == '__main__':
    # args: deploy local or remote
    deploy('http://localhost:8545')
