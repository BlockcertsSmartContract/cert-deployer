import json
import onchaining_tools.path_tools as tools
from web3 import Web3, HTTPProvider


class MakeW3:
    def __init__(self, chain):
        path = tools.get_chain_data_path()
        with open(path, "r") as raw_json:
            self.wallet_info = json.loads(raw_json.read())

        self.url = self.wallet_info[chain]["url"]
        self.privkey = self.wallet_info[chain]["privkey"]
        self.pubkey = self.wallet_info[chain]["pubkey"]

        self.w3 = self.create_w3_obj()

    def create_w3_obj(self):
        return Web3(HTTPProvider(self.url))

    def get_w3_obj(self):
        return self.w3

    def get_w3_wallet(self):
        return self.w3.eth.account.privateKeyToAccount(self.privkey)


class ContractConnection:
    def __init__(self, chain):
        self.w3 = MakeW3(chain).get_w3_obj()

        self.contract_info_path = contract_info_path
        self.contract_info = self.get_contract_info()

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

    def get_abi(self):
        return self.contract_info["abi"]

    def get_address(self):
        return self.contract_info["address"]
