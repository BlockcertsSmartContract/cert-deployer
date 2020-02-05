import json
import subprocess
import time
import logging
import config

from solc import compile_standard
from blockchain_handlers.namehash import namehash
from blockchain_handlers.connectors import MakeW3, ContractConnection
import blockchain_handlers.signer as signer
import blockchain_handlers.path_tools as tools

class ContractDeployer(object):
    '''
    Compiles, signes and deploys a smart contract on the ethereum blockchain
    '''
    def __init__(self):
        '''
        Defines blockchain, initializes ethereum wallet, calls out compilation
        and deployment functions
        '''
        self.parsed_config = config.get_config()
        w3Factory = MakeW3(self.parsed_config)
        self._w3 = w3Factory.w3
        self._acct = w3Factory.account
        self._pubkey = self.parsed_config.deploying_address
        self._ens_name = self.parsed_config.ens_name
        self.check_balance()

    def check_balance(self):
        gas_limit = 600000
        gas_price = self._w3.eth.gasPrice
        gas_balance = self._w3.eth.getBalance(self._pubkey)
        if gas_balance < gas_limit*gas_price:
            logging.error("Your gas balance is not sufficient for performing all transactions.")
            exit()

    def do_deploy(self):
        '''
        Starts deployment process step-by-step
        '''
        if self.parsed_config.chain == "ethereum_ropsten":
            ens_resolver = ContractConnection("ropsten_ens_resolver", self.parsed_config)
        elif self.parsed_config.chain == "ethereum_mainnet":
            ens_resolver = ContractConnection("mainnet_ens_resolver", self.parsed_config)

        node = namehash(self._ens_name)

        # check if ens address link should be changed intensionally
        temp = ens_resolver.functions.call("addr", node)
        if temp != "0x0000000000000000000000000000000000000000" and self.parsed_config.overwrite_ens_link != True:
            logging.error("Smart Contract already deployed on this domain and change_ens_link is not True.")
            exit("Stopping process.")

        self._compile_contract()
        self._deploy()
        try:
            self._update_ens_content()
        except:
            logging.error("There was a problem registering the ENS domain. Please re-run the deployer to make sure everything is set up properly.")

    def _compile_contract(self):
        '''
        Compiles smart contract, creates bytecode and abi
        '''
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
        '''
        Signes raw transaction and deploys it on the blockchain
        '''
        # building raw transaction
        contract = self._w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        estimated_gas = contract.constructor().estimateGas()
        construct_txn = contract.constructor().buildTransaction({
            'nonce': self._w3.eth.getTransactionCount(self._pubkey),
            'gas': estimated_gas*2
        })

        # signing & sending a signed transaction, saving transaction hash
        signed = signer.sign_transaction(self.parsed_config, construct_txn)
        logging.info("Transaction pending...")
        tx_hash = self._w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self._w3.eth.waitForTransactionReceipt(tx_hash)

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
        logging.info("Deployed the contract with hash: %s, and used the following amount of gas: %s.", self.contr_address, tx_receipt.gasUsed)

    def _update_ens_content(self):
        '''
        Starts ens updates
        '''
        if self.parsed_config.chain == "ethereum_ropsten" or self.parsed_config.chain == "ethereum_mainnet":
            self._assign_ens()

    def _assign_ens(self):
        # prepare domain
        ens_domain = self._ens_name
        node = namehash(ens_domain)

        # connect to registry and resolver
        if self.parsed_config.chain == "ethereum_ropsten":
            ens_registry = ContractConnection("ropsten_ens_registry", self.parsed_config)
            ens_resolver = ContractConnection("ropsten_ens_resolver", self.parsed_config)
            resolver_address = "0x42D63ae25990889E35F215bC95884039Ba354115"

        # this needs to be added to contr_info.json! Check mainnet resolver_address!
        elif self.parsed_config.chain == "ethereum_mainnet":
            ens_registry = ContractConnection("mainnet_ens_registry", self.parsed_config)
            ens_resolver = ContractConnection("mainnet_ens_resolver", self.parsed_config)
            resolver_address = "0x226159d592e2b063810a10ebf6dcbada94ed68b8ODO"

            # temporary – due to new registry contract
            # registry_address = "0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e"

        # set resolver
        ens_registry.functions.transact("setResolver", node, resolver_address)
        ens_registry.functions.transact("resolver", node)

        # set address
        self.contr_address = self._w3.toChecksumAddress(self.contr_address)
        ens_resolver.functions.transact("setAddr", node, self.contr_address)
        ens_resolver.functions.transact("setName", node, ens_domain)

        addr = ens_resolver.functions.call("addr", node)
        name = ens_resolver.functions.call("name", node)

        logging.info("Set contract %s to name %s.", addr, name)


if __name__ == '__main__':
    '''
    Calls respective functionatilites
    '''
    ContractDeployer().do_deploy()
