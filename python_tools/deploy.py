# Based on: https://web3py.readthedocs.io/en/stable/contracts.html

import json
import onchaining_tools.path_tools as tools
from onchaining_tools.connections import MakeW3
from solc import compile_standard


def compile_contract(w3Factory):
    w3 = w3Factory.get_w3_obj()
    acct = w3Factory.get_w3_wallet()

    with open(tools.get_contract_path()) as source_file:
        source_raw = source_file.read()

    with open(tools.get_compile_data_path()) as opt_file:
        raw_opt = opt_file.read()
        opt = json.loads(raw_opt)

    opt["sources"]["BlockCertsOnchaining.sol"]["content"] = source_raw
    compiled_sol = compile_standard(opt)
    bytecode = compiled_sol['contracts']['BlockCertsOnchaining.sol']['BlockCertsOnchaining']['evm']['bytecode']['object']
    abi = \
        json.loads(compiled_sol['contracts']['BlockCertsOnchaining.sol']['BlockCertsOnchaining']['metadata'])['output']['abi']

    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    acct_addr = w3Factory.pubkey

    construct_txn = contract.constructor().buildTransaction({
        'from': acct_addr,
        'nonce': w3.eth.getTransactionCount(acct_addr),
        #'gasPrice': w3.toWei('21', 'gwei')
    })

    signed = acct.signTransaction(construct_txn)
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    # tx_hash = contract.constructor().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    contr_address = tx_receipt.contractAddress
    blockcerts_onchaining = w3.eth.contract(address=contr_address, abi=abi)

    data = {'abi': abi, 'address': contr_address}

    with open(tools.get_config_data_path(), "w+") as outfile:
        json.dump(data, outfile)


    return blockcerts_onchaining


def deploy(chain):
    w3Factory = MakeW3(chain)
    compile_contract(w3Factory)


if __name__ == '__main__':
    # args: deploy local or remote
    deploy("ropsten")
