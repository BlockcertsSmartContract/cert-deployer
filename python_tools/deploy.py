# Based on: https://web3py.readthedocs.io/en/stable/contracts.html

import json
import onchaining_tools.path_tools as tools
import onchaining_tools.config as config
from onchaining_tools.connections import MakeW3
from solc import compile_standard


def compile_contract(w3Factory):
    ''' Compiles, signes and deploys a transaction on the ethereum blockchain
    Args:
        w3Factory(web3 object): instantiated web3 connection to ethereum node

    Returns:
        contr_adress(str): transaction adress on the blockchain
    '''

    '''getting data about wallet and ethereum node'''
    w3 = w3Factory.get_w3_obj()
    acct = w3Factory.get_w3_wallet()

    '''getting contract & configuration files paths'''
    with open(tools.get_contract_path()) as source_file:
        source_raw = source_file.read()

    with open(tools.get_compile_data_path()) as opt_file:
        raw_opt = opt_file.read()
        opt = json.loads(raw_opt)

    '''defining comppilation standart, abi and bytecode'''
    opt["sources"]["BlockCertsOnchaining.sol"]["content"] = source_raw
    compiled_sol = compile_standard(opt)
    bytecode = compiled_sol[
        'contracts']['BlockCertsOnchaining.sol']['BlockCertsOnchaining']['evm']['bytecode']['object']
    abi = json.loads(compiled_sol[
        'contracts']['BlockCertsOnchaining.sol']['BlockCertsOnchaining']['metadata'])['output']['abi']
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    '''getting data about ethereum chain and public key of the ethereum wallet, that will be used for the transaction'''
    current_chain = config.config["current_chain"]
    acct_addr = config.config["wallets"][current_chain]["pubkey"]

    '''creating a transaction'''
    construct_txn = contract.constructor().buildTransaction({
        # 'from': acct_addr,
        'nonce': w3.eth.getTransactionCount(acct_addr),
        'gasPrice': w3.toWei('50', 'gwei'),
        'gas': 1000000
    })
    '''signing raw transaction, sending it to the ethereum node and receiving the transaction hash'''
    signed = acct.signTransaction(construct_txn)
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    
    '''saving the data about transaction'''
    contr_address = tx_receipt.contractAddress
    data = {'abi': abi, 'address': contr_address}
    with open(tools.get_config_data_path(), "w+") as outfile:
        json.dump(data, outfile)

    return contr_address

if __name__ == '__main__':
    '''Calls out functions to create an ethereum node connection & to compile and to deploy a smart contract'''
    w3Factory = MakeW3()
    contract_address = compile_contract(w3Factory)
    print("deployed contract with address: " + str(contract_address))

