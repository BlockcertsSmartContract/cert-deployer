from web3 import Web3, HTTPProvider
from abc import ABC, abstractclassmethod
import json
# http://ropsten.infura.io/v3/a70de76e3fd748cbb6dbb2ed49dda183


class MakeW3:
    def __init__(self, url):
        self.url = url

    def get_w3_obj(self):
        w3 = Web3(HTTPProvider(self.url))
        return w3

    def set_w3_wallet(self, wallet_id=0):
        self.w3.eth.defaultAccount = self.w3.eth.accounts[wallet_id]


class ContractConnection(ABC):
    def __init__(self, url):
        self.url = url
        self.create_contract_object()
        self.contract_obj = self.get_contract_object()

    def create_contract_object(self):
        w3 = MakeW3(self.url).get_w3_obj()
        address = self.get_address()
        abi = self.get_abi()
        self.contract_obj = w3.eth.contract(address=address, abi=abi)

    def get_contract_object(self):
        return self.contract_obj

    @abstractclassmethod
    def get_abi(self):
        pass

    @abstractclassmethod
    def get_address(self):
        pass


# class SelfDeployedContract(ContractConnection):
    # pass


class TruffleContract(ContractConnection):
    """abstraction to create w3/contract object to access smart contract functions"""
    def __init__(self, url, contract_info_path):
        self.url = url
        self.contract_info_path = contract_info_path
        self.contract_info = self.get_contract_info()
        self.create_contract_object()
        self.contract_obj = self.get_contract_object()

    def get_contract_info(self):
        contract_info = ""
        with open(self.contract_info_path) as file:
            data = file.read()
            contract_info = json.loads(data)
        return contract_info

    def get_abi(self):
        return self.contract_info["abi"]

    def get_address(self):
        return self.contract_info["networks"]["5777"]["address"]
