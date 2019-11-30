# Based on: https://web3py.readthedocs.io/en/stable/contracts.html

import json
from typing import Any

from solc import compile_standard

import python_tools.onchaining_tools.tools as tools


def compile_contract(w3) -> Any:
    source_raw = ""
    with open(tools.get_root_dir() + "/contracts/BlockCertsOnchaining.sol") as source_file:
        source_raw = source_file.read()

    opt = ""
    with open(tools.get_root_dir() + "/data/compile_opt.json") as opt_file:
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
    block_certs_onchaining = w3.eth.contract(address=address, abi=abi)
    return block_certs_onchaining
