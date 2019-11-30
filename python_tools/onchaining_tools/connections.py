import json
from abc import ABC, abstractmethod

from web3 import Web3, HTTPProvider


# http://ropsten.infura.io/v3/a70de76e3fd748cbb6dbb2ed49dda183


class MakeW3:
    def __init__(self, url):
        self.url = url
        self.w3 = self.create_w3_obj()
        self.set_w3_wallet(0)

    def create_w3_obj(self):
        return Web3(HTTPProvider(self.url))

    def get_w3_obj(self):
        return self.w3

    def set_w3_wallet(self, wallet_id=0):
        self.w3.eth.defaultAccount = self.w3.eth.accounts[wallet_id]


class ContractConnection(ABC):
    def __init__(self, url):
        self.url = url
        self.w3 = MakeW3(self.url).get_w3_obj()
        self.create_contract_object()
        self.contract_obj = self.get_contract_object()

    def create_contract_object(self):
        address = self.get_address()
        abi = self.get_abi()
        self.contract_obj = self.w3.eth.contract(address=address, abi=abi)

    def get_contract_object(self):
        return self.contract_obj

    def get_contract_info(self):
        with open(self.contract_info_path) as file:
            data = file.read()
            contract_info = json.loads(data)
        return contract_info

    @abstractmethod
    def get_abi(self):
        pass

    @abstractmethod
    def get_address(self):
        pass


class SelfDeployedContract(ContractConnection):
    def __init__(self, url, contract_info_path):
        self.contract_info_path = contract_info_path
        self.contract_info = self.get_contract_info()
        super().__init__(url)

    def get_abi(self):
        return self.contract_info["abi"]

    def get_address(self):
        return self.contract_info["address"]


class TruffleContract(ContractConnection):
    def __init__(self, url, contract_info_path):
        self.contract_info_path = contract_info_path
        self.contract_info = self.get_contract_info()
        super().__init__(url)

    def get_abi(self):
        return self.contract_info["abi"]

    def get_address(self):
        return self.contract_info["networks"]["5777"]["address"]
