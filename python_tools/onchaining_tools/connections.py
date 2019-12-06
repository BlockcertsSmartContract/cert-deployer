import json

import onchaining_tools.config as config
import onchaining_tools.path_tools as tools
from web3 import Web3, HTTPProvider


class MakeW3(object):
    def __init__(self):
        self.privkey = config.config["wallets"][config.config["current_chain"]]["privkey"]
        self.pubkey = config.config["wallets"][config.config["current_chain"]]["pubkey"]
        self.url = config.config["wallets"][config.config["current_chain"]]["url"]
        self.w3 = self.create_w3_obj()
        self.w3.eth.defaultAccount = self.pubkey

    def create_w3_obj(self):
        return Web3(HTTPProvider(self.url))

    def get_w3_obj(self):
        return self.w3

    def get_w3_wallet(self):
        return self.w3.eth.account.from_key(self.privkey)


class ContractConnection(object):
    def __init__(self, contract_name):  # "blockcertsonchaining", "ropsten_ens_registry", "ropsten_ens_resolver"
        self.contract_name = contract_name
        self.w3 = MakeW3().get_w3_obj()
        self.contract_info = self.get_contract_info()
        self.contract_obj = self.create_contract_object()
        self.functions = ContractFunctions(self.w3, self.contract_obj)

    def create_contract_object(self):
        address = self.get_address()
        abi = self.get_abi()
        return self.w3.eth.contract(address=address, abi=abi)

    def get_contract_object(self):
        return self.contract_obj

    def get_contract_info(self):
        with open(tools.get_contr_info_path()) as file:
            data = file.read()
            contract_info = json.loads(data)
        return contract_info

    def get_abi(self):
        return self.contract_info[self.contract_name]["abi"]

    def get_address(self):
        return self.contract_info[self.contract_name]["address"]


class ContractFunctions(object):
    def __init__(self, w3, contract_obj):
        self.w3 = w3
        self.contract_obj = contract_obj

        current_chain = config.config["current_chain"]
        self.privkey = config.config["wallets"][current_chain]["privkey"]
        self.acct_addr = config.config["wallets"][current_chain]["pubkey"]

        print(self.contract_obj.all_functions())

    def get_tx_options(self):
        return {
            'nonce': self.w3.eth.getTransactionCount(self.acct_addr),
            'gasPrice': self.w3.toWei('50', 'gwei'),
            'gas': 1000000
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
