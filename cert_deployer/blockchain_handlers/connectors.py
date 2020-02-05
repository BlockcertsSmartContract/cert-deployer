import json
import logging

from web3 import Web3, HTTPProvider

import config
import blockchain_handlers.path_tools as tools
import blockchain_handlers.signer as signer


class MakeW3(object):
    '''
    Creates a w3 object
    '''
    def __init__(self, app_config):
        '''
        Defines an ethereum node that will be used for communication with the ethereum blockchain and initializes the account data
        '''
        current_chain = app_config.chain
        self._url = app_config.node_url

        self.w3 = self._create_w3_obj()
        self.account = app_config.deploying_address
        self.w3.eth.defaultAccount = self.account

    def _create_w3_obj(self):
        '''Instantiates a web3 connection with ethereum node'''
        return Web3(HTTPProvider(self._url))


class ContractConnection(object):
    '''
    Collects abi, address, contract data and instantiates a contract object
    '''
    def __init__(self, contract_name, app_config):
        self.contract_name = contract_name
        self._w3Factory = MakeW3(app_config)
        self.w3 = self._w3Factory.w3
        self._contract_info = self._get_contract_info()
        self.contract_obj = self._create_contract_object()
        self.functions = self.ContractFunctions(self._w3Factory, self.contract_obj, app_config)

    def _create_contract_object(self):
        '''
        Returns contract address and abi
        '''
        address = self._get_address()
        abi = self._get_abi()
        return self.w3.eth.contract(address=address, abi=abi)

    def _get_contract_info(self):
        '''
        Returns transaction data from a config file
        '''
        with open(tools.get_contr_info_path()) as file:
            data = file.read()
            contract_info = json.loads(data)
        return contract_info

    def _get_abi(self):
        '''
        Returns transaction abi
        '''
        return self._contract_info[self.contract_name]["abi"]

    def _get_address(self):
        '''
        Returns transaction address
        '''
        return self._contract_info[self.contract_name]["address"]


    class ContractFunctions(object):
        def __init__(self, w3Factory, contract_obj, app_config):
            self.app_config = app_config
            self._w3Factory = w3Factory
            self._w3 = self._w3Factory.w3
            self._contract_obj = contract_obj
            current_chain = app_config.chain
            self.acct = self._w3Factory.account
            self.acct_addr = app_config.deploying_address

        def _get_tx_options(self, estimated_gas):
            '''
            Returns raw transaction
            '''
            return {
                'nonce': self._w3.eth.getTransactionCount(self.acct_addr),
                'gas': estimated_gas*2
            }

        def transact(self, method, *argv):
            '''
            Sends a signed transaction on the blockchain and waits for a response
            '''
            # just temporal solution to avoid error
            estimated_gas = 2000000

            # gas estimation
            # estimated_gas = self._contract_obj.functions[method](*argv).estimateGas()
            logging.info('Estimated gas for %s: %s', str(method),str(estimated_gas))
            tx_options = self._get_tx_options(estimated_gas)

            # building a transaction
            construct_txn = self._contract_obj.functions[method](*argv).buildTransaction(tx_options)

            # signing a transaction
            signed = signer.sign_transaction(self.app_config, construct_txn)

            # sending a transaction to the blockchain and waiting for a response
            logging.info("Transaction %s pending...", str(method))
            tx_hash = self._w3.eth.sendRawTransaction(signed.rawTransaction)
            tx_receipt = self._w3.eth.waitForTransactionReceipt(tx_hash)
            logging.info("Executed transaction: %s, using the following amount of gas: %s", str(method), str(tx_receipt.gasUsed))

        def call(self, method, *argv):
            return self._contract_obj.functions[method](*argv).call()
