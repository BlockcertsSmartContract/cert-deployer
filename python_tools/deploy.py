import json
import onchaining_tools.config as config
import onchaining_tools.path_tools as tools
from onchaining_tools.connections import MakeW3, ContractConnection
from solc import compile_standard
from ens import ENS


class ContractDeployer(object):
    def __init__(self):
        current_chain = config.config["current_chain"]
        self.pubkey = config.config["wallets"][current_chain]["pubkey"]

        w3Factory = MakeW3()
        self.w3 = w3Factory.get_w3_obj()
        self.acct = w3Factory.get_w3_wallet()
        self.compile_contract()
        self.deploy()
        if current_chain == "ropsten":
            self.assign_ens()

    def compile_contract(self):
        with open(tools.get_contract_path()) as source_file:
            source_raw = source_file.read()

        with open(tools.get_compile_data_path()) as opt_file:
            raw_opt = opt_file.read()
            opt = json.loads(raw_opt)

        opt["sources"]["BlockCertsOnchaining.sol"]["content"] = source_raw
        compiled_sol = compile_standard(opt)
        self.bytecode = compiled_sol[
            'contracts']['BlockCertsOnchaining.sol']['BlockCertsOnchaining']['evm']['bytecode']['object']
        self.abi = json.loads(compiled_sol[
            'contracts']['BlockCertsOnchaining.sol']['BlockCertsOnchaining']['metadata'])['output']['abi']

    def deploy(self):
        contract = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)

        current_chain = config.config["current_chain"]
        acct_addr = config.config["wallets"][current_chain]["pubkey"]

        construct_txn = contract.constructor().buildTransaction({
            'nonce': self.w3.eth.getTransactionCount(acct_addr),
            'gas': 1000000
        })

        signed = self.acct.sign_transaction(construct_txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

        with open(tools.get_contr_info_path(), "r") as f:
            raw = f.read()
            contr_info = json.loads(raw)

        self.contr_address = tx_receipt.contractAddress
        data = {'abi': self.abi, 'address': self.contr_address}
        contr_info["blockcertsonchaining"] = data

        with open(tools.get_contr_info_path(), "w+") as f:
            json.dump(contr_info, f)

        print(f"deployed contr <{self.contr_address}>")

    def assign_ens(self):
        ens_domain = "blockcerts.eth"
        ens_resolver = ContractConnection("ropsten_ens_resolver")

        # for testing purposes
        # self.contr_address = "0x01a616157b59d75a1d62f3913c105f443232a1f6"
        self.contr_address = self.w3.toChecksumAddress(self.contr_address)

        ns = ENS.fromWeb3(self.w3)
        node = ns.namehash(ens_domain)

        ens_resolver.functions.transact("setAddr", node, self.contr_address)
        ens_resolver.functions.transact("setName", node, ens_domain)

        addr = ens_resolver.functions.call("addr", node)
        name = ens_resolver.functions.call("name", node)

        print(f"set contr <{addr}> to name '{name}'")


if __name__ == '__main__':
    ContractDeployer()
