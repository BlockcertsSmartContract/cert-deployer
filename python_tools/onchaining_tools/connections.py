import json
from abc import ABC, abstractmethod

from web3 import Web3, HTTPProvider


# http://ropsten.infura.io/v3/a70de76e3fd748cbb6dbb2ed49dda183


class MakeW3:
    def __init__(self, url) -> None:
        self.url = url
        self.w3 = self.create_w3_obj()
        self.set_w3_wallet(0)

    def create_w3_obj(self) -> Web3:
        return Web3(HTTPProvider(self.url))

    def get_w3_obj(self) -> Web3:
        return self.w3

    def set_w3_wallet(self, wallet_id=0) -> None:
        self.w3.eth.defaultAccount = self.w3.eth.accounts[wallet_id]


class ContractConnection(ABC):
    def __init__(self, url) -> None:
        self.url = url
        self.w3 = MakeW3(self.url).get_w3_obj()
        self.create_contract_object()
        self.contract_obj = self.get_contract_object()

    def create_contract_object(self) -> None:
        address = self.get_address()
        abi = self.get_abi()
        self.contract_obj = self.w3.eth.contract(address=address, abi=abi)

    def get_contract_object(self) -> Web3:
        return self.contract_obj

    @abstractmethod
    def get_abi(self) -> None:
        pass

    @abstractmethod
    def get_address(self) -> None:
        pass


class TruffleContract(ContractConnection):
    """abstraction to create w3/contract object to access smart contract functions"""

    def __init__(self, url, contract_info_path) -> None:
        self.url = url
        self.contract_info_path = contract_info_path
        self.contract_info = self.get_contract_info()
        self.w3 = MakeW3(self.url).get_w3_obj()
        self.create_contract_object()
        self.contract_obj = self.get_contract_object()

    def get_contract_info(self) -> str:
        contract_info = ""
        with open(self.contract_info_path) as file:
            data = file.read()
            contract_info = json.loads(data)
        return contract_info

    def get_abi(self) -> str:
        return self.contract_info["abi"]

    def get_address(self) -> str:
        return self.contract_info["networks"]["5777"]["address"]
