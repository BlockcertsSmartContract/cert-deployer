import json
import subprocess
import time
import logging
import content_hash

from solc import compile_standard
from blockchain_handlers.namehash import namehash
import blockchain_handlers.path_tools as tools
from blockchain_handlers.connections import MakeW3, ContractConnection
import config

class ContractDeployer(object):
    ''' Compiles, signes and deploys a smart contract on the ethereum blockchain '''

    def __init__(self):
        '''Defines blockchain, initializes ethereum wallet, calls out compilation and deployment functions'''
        self.parsed_config = config.get_config()
        self.current_chain = self.parsed_config.chain
        self.ens_name = self.parsed_config.ens_name
        w3Factory = MakeW3(self.parsed_config)
        self._w3 = w3Factory.w3
        self._acct = w3Factory.account
        self._pubkey = self._acct.address
        #self.check_balance()

    def check_balance(self):
        gas_limit = 600000
        gas_price = self._w3.eth.gasPrice
        gas_balance = self._w3.eth.getBalance(self._pubkey)
        print(loft)
        if gas_balance < gas_limit*gas_price:
            exit('Your gas balance is not sufficient for performing all transactions.')

    def do_deploy(self):
        # self._compile_contract()
        # self._deploy()
        self._update_ens_content()

    def _compile_contract(self):
        '''Compiles smart contract, creates bytecode and abi'''
        # loading contract file data
        with open(tools.get_contract_path()) as source_file:
            source_raw = source_file.read()

        # loading configuration data
        with open(tools.get_compile_data_path()) as opt_file:
            raw_opt = opt_file.read()
            opt = json.loads(raw_opt)

        opt["sources"]["BlockCertsOnchaining.sol"]["content"] = source_raw
        compiled_sol = compile_standard(opt)

        # defining bytecode and abi
        self.bytecode = compiled_sol[
            'contracts']['BlockCertsOnchaining.sol']['BlockCertsOnchaining']['evm']['bytecode']['object']
        self.abi = json.loads(compiled_sol[
                                  'contracts']['BlockCertsOnchaining.sol']['BlockCertsOnchaining']['metadata'])[
            'output']['abi']

    def _deploy(self):
        '''Signes raw transaction and deploys it on the blockchain'''
        contract = self._w3.eth.contract(abi=self.abi, bytecode=self.bytecode)

        # defining blockchain and public key of the ethereum wallet
        acct_addr = self._pubkey

        # building raw transaction
        estimated_gas = contract.constructor().estimateGas()
        construct_txn = contract.constructor().buildTransaction({
            'nonce': self._w3.eth.getTransactionCount(acct_addr),
            'gas': estimated_gas*2
        })

        # signing & sending a signed transaction, saving transaction hash
        signed = self._acct.sign_transaction(construct_txn)
        tx_hash = self._w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self._w3.eth.waitForTransactionReceipt(tx_hash)
        logging.info('Gas used: %s', tx_receipt.gasUsed)

        # saving contract data
        with open(tools.get_contr_info_path(), "r") as f:
            raw = f.read()
            contr_info = json.loads(raw)

        self.contr_address = tx_receipt.contractAddress
        data = {'abi': self.abi, 'address': self.contr_address}
        contr_info["blockcertsonchaining"] = data

        with open(tools.get_contr_info_path(), "w+") as f:
            json.dump(contr_info, f)

        # print transaction hash
        logging.info("deployed contr %s", self.contr_address)

    def _update_ens_content(self):
        if self.current_chain == "ethereum_ropsten" or self.current_chain == "ethereum_mainnet":
            self._assign_ens()

    def _assign_ens(self):
        ens_domain = self.parsed_config.ens_name
        ens_registry = ContractConnection("ropsten_ens_registry", self.parsed_config)
        node = namehash(ens_domain)

        #set resolver
        ens_registry.functions.transact("setResolver", node, "0x12299799a50340FB860D276805E78550cBaD3De3")

        #set Address
        ens_resolver = ContractConnection("ropsten_ens_resolver", self.parsed_config)
        self.contr_address = self._w3.toChecksumAddress(self.contr_address)
        ens_resolver.functions.transact("setAddr", node, self.contr_address)
        ens_resolver.functions.transact("setName", node, ens_domain)

        addr = ens_resolver.functions.call("addr", node)
        name = ens_resolver.functions.call("name", node)

        content = "none"
        if self._client is not None:
            content = (ens_resolver.functions.call("contenthash", node)).hex()
            content = content_hash.decode(content)

        logging.info('set contr %s to name %s with content %s', addr, name, content)

if __name__ == '__main__':
    ''' Calls respective functionatilites. '''
    ContractDeployer().do_deploy()
