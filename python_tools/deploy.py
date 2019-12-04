# Based on: https://web3py.readthedocs.io/en/stable/contracts.html

import json
import onchaining_tools.path_tools as tools
import onchaining_tools.config as config
from onchaining_tools.connections import MakeW3
from solc import compile_standard
from ens import ENS


def compile_contract(w3Factory):
    w3 = w3Factory.get_w3_obj()
    acct = w3Factory.get_w3_wallet()

    #ns object necessary for ENS calls with connection to ropsten registry
    ns = ENS.fromWeb3(w3, "0x112234455C3a32FD11230C42E7Bccd4A84e02010")

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
    acct_addr = config.config["wallets"][current_chain]["pubkey"]#["ens"]

    construct_txn = contract.constructor().buildTransaction({
        'from': acct_addr,
        'nonce': w3.eth.getTransactionCount(acct_addr),
        'gasPrice': w3.toWei('50', 'gwei'),
        'gas': 1000000
    })

    signed = acct.signTransaction(construct_txn)
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    contr_address = tx_receipt.contractAddress
    data = {'abi': abi, 'address': contr_address}

    with open(tools.get_config_data_path(), "w+") as outfile:
        json.dump(data, outfile)

    #find ens domain according to wallet and store new contract at domain 
    name = ns.name(str(config.config["wallets"][config.config["current_chain"]]["pubkey"]))

    #TODO
    ns.setup_addres(name, contr_address)

    print("deployed contract with address: " + str(contr_address) + ", and ENS Entry at Domain: " + name)

if __name__ == '__main__':
    w3Factory = MakeW3()
    compile_contract(w3Factory)
