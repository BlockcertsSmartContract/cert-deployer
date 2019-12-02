import json
import onchaining_tools.config as config
import onchaining_tools.path_tools as tools
from web3 import Web3, HTTPProvider


class MakeW3:
    def __init__(self):
        self.privkey = config.config["wallets"][config.config["currentChain"]]["privkey"]
        self.url = config.config["wallets"][config.config["currentChain"]]["url"]
        self.w3 = self.create_w3_obj()

    def create_w3_obj(self):
        return Web3(HTTPProvider(self.url))

    def get_w3_obj(self):
        return self.w3

    def get_w3_wallet(self):
        return self.w3.eth.account.privateKeyToAccount(self.privkey)


class ContractConnection:
    def __init__(self):
        chain = config.config["currentChain"]
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
        with open(tools.get_config_data_path()) as file:
            data = file.read()
            contract_info = json.loads(data)
        return contract_info

    def get_abi(self):
        return self.contract_info["abi"]

    def get_address(self):
        return self.contract_info["address"]

class ContractFunctions:
    def __init__(self, w3, contract_obj):
        self.w3 = w3
        self.contract_obj = contract_obj

        currentChain = config.config["currentChain"]
        self.privkey = config.config["wallets"][currentChain]["privkey"]
        self.acct_addr = config.config["wallets"][currentChain]["pubkey"]

    def issue(self, hashVal):
        acct = self.w3.eth.account.privateKeyToAccount(self.privkey)

        construct_txn = self.contract_obj.functions.issueHash(hashVal).buildTransaction({
            'nonce': self.w3.eth.getTransactionCount(self.acct_addr),
            'gasPrice': self.w3.toWei('50', 'gwei'),
            'gas': 1000000
        })

        signed = acct.signTransaction(construct_txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

    def revoke(self, hashVal):
        acct = self.w3.eth.account.privateKeyToAccount(self.privkey)

        construct_txn = self.contract_obj.functions.revokeHash(hashVal).buildTransaction({
            'nonce': self.w3.eth.getTransactionCount(self.acct_addr),
            'gasPrice': self.w3.toWei('50', 'gwei'),
            'gas': 1000000
        })

        signed = acct.signTransaction(construct_txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

    def getStatus(self, hash_val):
        return self.contract_obj.functions.hashes(hash_val).call()



    # def constructor(self):
        # contract = w3.eth.contract(abi=abi, bytecode=bytecode)

        # acct_addr = w3Factory.pubkey

        # construct_txn = contract.constructor().buildTransaction({
            # # 'from': acct_addr,
            # 'nonce': w3.eth.getTransactionCount(acct_addr),
            # 'gasPrice': w3.toWei('50', 'gwei')
        # })

        # signed = acct.signTransaction(construct_txn)
        # tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
        # # tx_hash = contract.constructor().transact()
        # tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        # contr_address = tx_receipt.contractAddress





