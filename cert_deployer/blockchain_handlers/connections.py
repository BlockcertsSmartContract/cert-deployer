import json

from web3 import Web3, HTTPProvider

import blockchain_handlers.path_tools as tools
import config
import os

def get_secret(parsed_config):
    path_to_secret = os.path.join(parsed_config.usb_name, parsed_config.key_file)

    with open(path_to_secret) as key_file:
        key = key_file.read().strip()
    return key

class MakeW3(object):
    '''
    Defines a private key of an ethereum wallet to be used for the transaction,
    node url to be used for communication with ethereum blockchain and instantiates the
    web3 connection with ethereum node
    '''
    def __init__(self, parsed_config):
        '''
        Defines public & private keys of a wallet, defines an ethereum node
        that will be used for communication with blockchain
        '''
        current_chain = parsed_config.chain
        self._privkey = get_secret(parsed_config)
        self._url = parsed_config.infura_node

        self.w3 = self._create_w3_obj()
        self.account = self._get_w3_wallet()
        self.pubkey = parsed_config.deploying_address
        self.w3.eth.defaultAccount = self.pubkey

    def _create_w3_obj(self):
        '''Instantiates a web3 connection with ethereum node'''
        return Web3(HTTPProvider(self._url))

    #do we still want to do that? wouldnt it be safer to just use the pubkey we have anyway?
    def _get_w3_wallet(self):
        '''Connects a private key to the account that is going to be used for the transaction'''
        return self.w3.eth.account.from_key(self._privkey)


class ContractConnection(object):
    '''Collects abi, address, contract data and instantiates a contract object'''
    def __init__(self, contract_name, parsed_config):
        self.contract_name = contract_name
        self._w3Factory = MakeW3(parsed_config)
        self.w3 = self._w3Factory.w3
        self._contract_info = self._get_contract_info()
        self.contract_obj = self._create_contract_object()
        self.functions = self.ContractFunctions(self._w3Factory, self.contract_obj, parsed_config)

    def _create_contract_object(self):
        '''Returns contract address and abi'''
        address = self._get_address()
        abi = self._get_abi()
        return self.w3.eth.contract(address=address, abi=abi)

    def _get_contract_info(self):
        '''Returns transaction data from a config file'''
        with open(tools.get_contr_info_path()) as file:
            data = file.read()
            contract_info = json.loads(data)
        return contract_info

    def _get_abi(self):
        '''Returns transaction abi'''
        return self._contract_info[self.contract_name]["abi"]

    def _get_address(self):
        '''Returns transaction address'''
        return self._contract_info[self.contract_name]["address"]

    class ContractFunctions(object):
        def __init__(self, w3Factory, contract_obj, parsed_config):
            self._w3Factory = w3Factory
            self._w3 = self._w3Factory.w3
            self._contract_obj = contract_obj
            current_chain = parsed_config.chain
            self._privkey = get_secret(parsed_config)
            self.acct = self._w3Factory.account
            self.acct_addr = self.acct.address

        def _get_tx_options(self, estimated_gas):
            '''Returns raw transaction'''
            return {
                'nonce': self._w3.eth.getTransactionCount(self.acct_addr),
                'gas': estimated_gas*2
            }

        def transact(self, method, *argv):
            '''Sends a signed transaction on the blockchain and waits for a response'''
            # gas estimation
            estimated_gas = self._contract_obj.functions[method](*argv).estimateGas()
            print("Estimated gas for " + str(method) + ": " + str(estimated_gas))
            tx_options = self._get_tx_options(estimated_gas)
            # building a transaction
            construct_txn = self._contract_obj.functions[method](*argv).buildTransaction(tx_options)
            # signing a transaction
            signed = self.acct.sign_transaction(construct_txn)
            # sending a transaction to the blockchain and waiting for a response
            tx_hash = self._w3.eth.sendRawTransaction(signed.rawTransaction)
            tx_receipt = self._w3.eth.waitForTransactionReceipt(tx_hash)
            print("Gas used: " + str(method) + ": " + str(tx_receipt.gasUsed))

        def call(self, method, *argv):
            return self._contract_obj.functions[method](*argv).call()