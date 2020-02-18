import json
import logging
import config

from solc import compile_standard
# from blockchain_handlers.namehash import namehash
from ens import ENS
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
        self.app_config = config.get_config()
        w3Factory = MakeW3(self.app_config)
        self._w3 = w3Factory.w3
        self._acct = w3Factory.account
        self._pubkey = self.app_config.deploying_address
        self._ens_name = self.app_config.ens_name

    def check_balance(self):
        estimated_required_gas = 400000
        gas_price = self._w3.eth.gasPrice

        gas_balance = self._w3.eth.getBalance(self._pubkey)
        if gas_balance < estimated_required_gas * gas_price:
            logging.error("Your account balance is not sufficient to perform all transactions.")
            exit()

    def do_deploy(self):
        '''
        Guides the deployment process step-by-step
        '''
        self.check_balance()
        self._security_check()
        self._compile_contract()
        self._deploy()
        self._assign_ens()

    def _security_check(self):
        '''
        Makes sure that an existing contract does not get overwritten unintensionally
        '''
        # connect to public resolver
        ens_resolver = ContractConnection("ens_resolver", self.app_config)
        node = ENS.namehash(self._ens_name)
        temp = ens_resolver.functions.call("addr", node)

        # check if ens address is already linked to a contract
        if temp != "0x0000000000000000000000000000000000000000" and self.app_config.overwrite_ens_link is not True:
            logging.error("A smart Contract already deployed on this domain and change_ens_link is not True.")
            exit("Stopping process.")

    def _compile_contract(self):
        '''
        Compiles smart contract, creates bytecode and abi
        '''
        # loading contract file data
        with open(tools.get_contr_path()) as source_file:
            source_raw = source_file.read()

        # loading configuration data
        with open(tools.get_compile_data_path()) as opt_file:
            raw_opt = opt_file.read()
            opt = json.loads(raw_opt)

        opt["sources"]["CertificateStore.sol"]["content"] = source_raw
        compiled_sol = compile_standard(opt)

        # defining bytecode and abi
        self.bytecode = compiled_sol[
            'contracts']['CertificateStore.sol']['CertificateStore']['evm']['bytecode']['object']
        self.abi = json.loads(compiled_sol[
                                  'contracts']['CertificateStore.sol']['CertificateStore']['metadata'])['output']['abi']

        with open(tools.get_contr_info_path(), "w+") as f:
            json.dump(self.abi, f)

        logging.info("Succesfully compiled contract")

    def _deploy(self):
        '''
        Signes raw transaction and deploys contract on the blockchain
        '''
        # building raw transaction
        contract = self._w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        estimated_gas = contract.constructor().estimateGas()
        construct_txn = contract.constructor().buildTransaction({
            'nonce': self._w3.eth.getTransactionCount(self._pubkey),
            'gas': estimated_gas*2
        })

        # signing and sending transaction
        signed = signer.sign_transaction(self.app_config, construct_txn)
        logging.info("Deployment pending...")
        # try:
        tx_hash = self._w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self._w3.eth.waitForTransactionReceipt(tx_hash)
        self.contr_address = tx_receipt.contractAddress
        # print transaction hash
        logging.info("Deployed the contract at address %s, and used %s gas.", self.contr_address, tx_receipt.gasUsed)

    def _assign_ens(self):
        '''
        Updates ENS entries
        '''
        # prepare domain
        ens_domain = self._ens_name
        node = ENS.namehash(ens_domain)

        # connect to registry and resolver
        ens_registry = ContractConnection("ens_registry", self.app_config)
        ens_resolver = ContractConnection("ens_resolver", self.app_config)

        # set resolver
        curr_resolver = ens_registry.functions.call("resolver", node)
        if curr_resolver == "0x0000000000000000000000000000000000000000":
            resolver_address = ContractConnection.get_ens_address(self.app_config.chain, "ens_resolver")
            ens_registry.functions.transact("setResolver", node, resolver_address)
        else:
            logging.info("Resolver already set for %s.", ens_domain)

        # set ABI
        ens_resolver.functions.transact("setABI", node, 1, json.dumps(self.abi).encode())
        print(ens_resolver.functions.call("ABI", node, 1))

        # set address
        self.contr_address = self._w3.toChecksumAddress(self.contr_address)
        ens_resolver.functions.transact("setAddr", node, self.contr_address)
        ens_resolver.functions.transact("setName", node, ens_domain)

        # get data for output
        addr = ens_resolver.functions.call("addr", node)
        name = ens_resolver.functions.call("name", node)

        # not working yet
        # ens_resolver.functions.transact("setABI", node, 0, json.dumps(self.abi).encode('utf-8'))

        logging.info("Set contract with address %s to name %s.", addr, name)


if __name__ == '__main__':
    '''
    Calls respective functionatilites
    '''
    ContractDeployer().do_deploy()
