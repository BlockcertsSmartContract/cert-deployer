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
        self.url = config.config["wallets"][config.config["current_chain"]]["url"]
        self.w3 = self.create_w3_obj()
        account = self.get_w3_wallet()
        self.pubkey = account.address
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

        self.privkey = config.config["wallets"][config.config["current_chain"]]["privkey"]
        account = self.w3.eth.account.from_key(self.privkey)
        self.acct_addr = account.address


    def get_tx_options(self, estimated_gas):
        '''Returns raw transaction'''
        
        return {
            'nonce': self.w3.eth.getTransactionCount(self.acct_addr),
            'gas': estimated_gas
        }

    def transact(self, method, *argv):
        acct = self.w3.eth.account.from_key(self.privkey)
        #gas estimation
        estimated_gas = self.contract_obj.functions[method](*argv).estimateGas()
        print("Estimated gas for " + str(method) + ": " + str(estimated_gas))
        tx_options = self.get_tx_options(estimated_gas)
        #building a transaction
        construct_txn = self.contract_obj.functions[method](*argv).buildTransaction(tx_options)
        #signing a transaction
        signed = acct.sign_transaction(construct_txn)
        #sendint a transaction to the blockchain and waiting for a response
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        print("Gas used: " + str(method) + ": " + str(tx_receipt.gasUsed))


    def constructor(self):
        acct = self.w3.eth.account.from_key(self.privkey)
        tx_options = self.get_tx_options()
        construct_txn = self.contract_obj.constructor().buildTransaction(tx_options)
        signed = acct.sign_transaction(construct_txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        self.w3.eth.waitForTransactionReceipt(tx_hash)
        

    def call(self, method, *argv):
        return self.contract_obj.functions[method](*argv).call()
