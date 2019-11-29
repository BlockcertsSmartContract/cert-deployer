# Based on: https://web3py.readthedocs.io/en/stable/contracts.html

import json
from solc import compile_standard
from web3 import Web3


def compile_contract():
    source_raw = ""
    with open("/home/xenia/Documents/PAS/BlockCerts/BlockCertsOnchainingEth/contracts/BlockCertsOnchaining.sol") as source_file:
        source_raw = source_file.read()

    opt = ""
    with open("/home/xenia/Documents/PAS/BlockCerts/BlockCertsOnchainingEth/data/compile_opt.json") as opt_file:
        raw_opt = opt_file.read()
        opt = json.loads(raw_opt)

    opt["sources"]["BlockCertsOnchaining.sol"]["content"] = source_raw

    compiled_sol = compile_standard(opt)

    #bytecode = compiled_sol['contracts']['BlockCertsOnchaining.sol']['BlockCertsOnchaining']['evm']['bytecode']['object']
    #abi = json.loads(compiled_sol['contracts']['BlockCertsOnchaining.sol']['BlockCertsOnchaining']['metadata'])['output']['abi']

    w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/hqRzEqFKv6IsjRxfVUWH"))

    abi = json.loads(compiled_sol['contracts']['BlockCertsOnchaining.sol']['BlockCertsOnchaining']['metadata'])['output']['abi']
    bytecode = compiled_sol['contracts']['BlockCertsOnchaining.sol']['BlockCertsOnchaining']['evm']['bytecode']['object']

    contract_ = w3.eth.contract(abi=abi, bytecode=bytecode)
    acct = w3.eth.account.privateKeyToAccount("3ADD48CBFFECF312C634ACDA0EC1268D7982DB067F135A2FB37309A8659F3D2F")
    construct_txn = contract_.constructor().buildTransaction({
        'from': "0x09eD136C76053F14345b801aA944525a560CC44c",
        'nonce': w3.eth.getTransactionCount("0x09eD136C76053F14345b801aA944525a560CC44c"),
        'gas': 1728712,
        'gasPrice': w3.toWei('21', 'gwei')})

    signed = acct.signTransaction(construct_txn)

    w3.eth.sendRawTransaction(signed.rawTransaction)
    
    

    #contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    #tx_hash = contract.constructor().transact()
    #tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    #address = tx_receipt.contractAddress
    #blockCertsOnchaining = w3.eth.contract(address=address, abi=abi)
    #return blockCertsOnchaining

#w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/hqRzEqFKv6IsjRxfVUWH"))

compile_contract()