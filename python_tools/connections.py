#! /usr/bin/python

from web3 import Web3, HTTPProvider
import json

class ContractConnection:
    """abstraction to create w3/contract object to access smart contract functions TODO: support for ropsten/mainnet ethereum networks"""
    def __init__(self, contract_url, contract_info_path):
        self.contract_url = contract_url
        self.contract_info_path = contract_info_path
        self.contract_info = self.get_contract_info()
        self.contract_obj = self.create_contract_object()
        print("ContractConnection: initialized")

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
        self.w3 = Web3(HTTPProvider(self.contract_url))
        self.set_w3_wallet()

    def set_w3_wallet(self, wallet_id = 0):
        self.w3.eth.defaultAccount = self.w3.eth.accounts[wallet_id]
        print("ContractConnection: set active wallet to " + str(self.w3.eth.accounts[wallet_id]))

    def create_contract_object(self):
        self.create_w3_object()
        address = self.get_contract_address()
        abi = self.get_contract_abi()
        print("ContractConnection: created interface to contract at address: " + str(address))
        return self.w3.eth.contract(address = address, abi = abi)

    def get_contract_object(self):
        return self.contract_obj
