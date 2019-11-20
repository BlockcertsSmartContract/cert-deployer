#! /usr/bin/python

from web3 import Web3, HTTPProvider
import json

class ContractConnection:
    def __init__(self, contract_url, contract_info_path):
        self.contract_url = contract_url
        self.contract_info_path = contract_info_path
        self.contract_info = self.get_contract_info()

    def get_contract_info(self):
        contract_info = ""
        with open(self.contract_info_path) as file:
            data = file.read()
            contract_info = json.loads(data)
        return contract_info

    def get_contract_abi(self):
        return self.contract_info["abi"]

    def get_contract_address(self):
        return self.contract_info["networks"]["5777"]["address"]

    def create_w3_object(self):
        w3 = Web3(HTTPProvider(self.contract_url))
        w3.eth.defaultAccount = w3.eth.accounts[0]
        return w3

    def create_contract_object(self):
        w3 = self.create_w3_object()
        return w3.eth.contract(address = self.get_contract_address(), abi = self.get_contract_abi())
