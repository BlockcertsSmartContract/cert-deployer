import json

import onchaining_tools.config as config
import onchaining_tools.path_tools as tools
from web3 import Web3, HTTPProvider


class MakeW3(object):
    '''Defines a private key of an ethereum wallet to be used for the transaction, 
        node url to be used for communication with ethereum blockchain and instantiates the
        web3 connection with ethereum node '''
    def __init__(self):
        '''Defines public & private keys of a wallet, defines an ethereum node, that will be used for communication with blockchain'''
        self.privkey = config.config["wallets"][config.config["current_chain"]]["privkey"]
        self.pubkey = config.config["wallets"][config.config["current_chain"]]["pubkey"]
        self.url = config.config["wallets"][config.config["current_chain"]]["url"]
        self.w3 = self.create_w3_obj()
        self.w3.eth.defaultAccount = self.pubkey

    def create_w3_obj(self):
        '''Instantiates a web3 connection with ethereum node'''
        return Web3(HTTPProvider(self.url))

    def get_w3_obj(self):
        return self.w3

    def get_w3_wallet(self):
        '''Connects a private key to the account that is going to be used for the transaction'''
        return self.w3.eth.account.from_key(self.privkey)


class ContractConnection(object):
    '''Collects abi, address, contract data and instantiates a contract object'''
    def __init__(self, contract_name="ropsten"): 
        self.contract_name = contract_name
        self.w3 = MakeW3().get_w3_obj()
        self.contract_info = self.get_contract_info()
        self.contract_obj = self.create_contract_object()
        self.functions = ContractFunctions(self.w3, self.contract_obj)

    def create_contract_object(self):
        '''Returns contract address and abi'''
        address = self.get_address()
        abi = self.get_abi()
        return self.w3.eth.contract(address=address, abi=abi)

    def get_contract_object(self):
        '''Returns instantiated contract'''
        return self.contract_obj

    def get_contract_info(self):
        '''Returns transaction data from a config file'''
        with open(tools.get_contr_info_path()) as file:
            data = file.read()
            contract_info = json.loads(data)
        return contract_info

    def get_abi(self):
        '''Returns transaction abi'''
        return self.contract_info[self.contract_name]["abi"]

    def get_address(self):
        '''Returns transaction address'''
        return self.contract_info[self.contract_name]["address"]


class ContractFunctions(object):
    def __init__(self, w3, contract_obj):
        self.w3 = w3
        self.contract_obj = contract_obj

        current_chain = config.config["current_chain"]
        self.privkey = config.config["wallets"][current_chain]["privkey"]
        self.acct_addr = config.config["wallets"][current_chain]["pubkey"]

    def get_tx_options(self):
        '''Returns raw transaction'''
        return {
            'nonce': self.w3.eth.getTransactionCount(self.acct_addr),
            'gas': 100000
            # 'gas': self.contract_obj.functions[method](*argv).estimateGas(),  # not working yet
        }

    def transact(self, method, *argv):
        acct = self.w3.eth.account.from_key(self.privkey)
        tx_options = self.get_tx_options()
        construct_txn = self.contract_obj.functions[method](*argv).buildTransaction(tx_options)
        signed = acct.sign_transaction(construct_txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        self.w3.eth.waitForTransactionReceipt(tx_hash)

    def constructor(self):
        acct = self.w3.eth.account.from_key(self.privkey)
        tx_options = self.get_tx_options()
        construct_txn = self.contract_obj.constructor().buildTransaction(tx_options)
        signed = acct.sign_transaction(construct_txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        self.w3.eth.waitForTransactionReceipt(tx_hash)

    def call(self, method, *argv):
        return self.contract_obj.functions[method](*argv).call()
