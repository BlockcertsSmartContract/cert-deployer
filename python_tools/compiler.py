# Based on: https://web3py.readthedocs.io/en/stable/contracts.html

import json
from solc import compile_standard
from web3 import Web3


def compile_contract(w3):
    source_raw = ""
    with open("/home/xenia/Documents/PAS/BlockCerts/BlockCertsOnchainingEth/contracts/BlockCertsOnchaining.sol") as source_file:
        source_raw = source_file.read()

    opt = ""
    with open("/home/xenia/Documents/PAS/BlockCerts/BlockCertsOnchainingEth/data/compile_opt.json") as opt_file:
        raw_opt = opt_file.read()
        opt = json.loads(raw_opt)

    opt["sources"]["BlockCertsOnchaining.sol"]["content"] = source_raw

    #define compiling standart
    compiled_sol = compile_standard(opt)

    #define bytecode
    bytecode = compiled_sol['contracts']['BlockCertsOnchaining.sol']['BlockCertsOnchaining']['evm']['bytecode']['object']

    #define abi
    abi = json.loads(compiled_sol['contracts']['BlockCertsOnchaining.sol']['BlockCertsOnchaining']['metadata'])['output']['abi']
    

    contract_ = w3.eth.contract(abi=abi, bytecode=bytecode)

    #ask for public key, first withou error handling
    pubkey = input("Please enter public key of your Ethereum wallet: \n")
    privkey = input("Please enter private key of your Ethereum wallet: \n")

    #set privatekey
    acct = w3.eth.account.privateKeyToAccount(privkey)
    
    #create unsigned transaction
    construct_txn = contract_.constructor().buildTransaction({
        'from': pubkey,
        'nonce': w3.eth.getTransactionCount(pubkey),
        })

    #sign transaction
    signed = acct.signTransaction(construct_txn)

    #send transaction to blockchain, returns transaction hash 
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)

    #convert transaction hash to hexa 
    print("Smart contract successfully deployed! Transaction hash: " + w3.toHex(tx_hash))
