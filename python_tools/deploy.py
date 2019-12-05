import json
import onchaining_tools.config as config
import onchaining_tools.path_tools as tools
from onchaining_tools.connections import MakeW3
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
            # 'from': acct_addr,
            'nonce': self.w3.eth.getTransactionCount(acct_addr),
            'gas': 1000000
        })

        signed = self.acct.sign_transaction(construct_txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

        self.contr_address = tx_receipt.contractAddress
        data = {'abi': self.abi, 'address': self.contr_address}

        with open(tools.get_contr_info_path(), "w+") as outfile:
            json.dump(data, outfile)

        print(f"deployed contr <{self.contr_address}>")

    def assign_ens(self):
        with open(tools.get_contr_info_path()) as f:
            contr_info_raw = f.read()
        contr_info = json.loads(contr_info_raw)
        self.contr_address = contr_info["address"]

        ns = ENS.fromWeb3(self.w3, "0x112234455C3a32FD11230C42E7Bccd4A84e02010")

        ens_path = tools.get_ens_abi_path()
        with open(ens_path) as f:
            ens_abi = f.read()

        abi = json.loads(ens_abi)

        address = "0x112234455C3a32FD11230C42E7Bccd4A84e02010"  # registry addr
        address = "0x12299799a50340FB860D276805E78550cBaD3De3"  # resolver addr
        address = self.w3.toChecksumAddress(address)

        node = ns.namehash("blockcerts.eth")
        self.contr_address = self.w3.toChecksumAddress(self.contr_address)

        contract = self.w3.eth.contract(address=address, abi=abi)

        construct_txn = contract.functions["setAddr"](node, self.contr_address).buildTransaction({
            'from': self.pubkey,
            'nonce': self.w3.eth.getTransactionCount(self.pubkey),
            'gas': 1000000
        })

        signed = self.acct.signTransaction(construct_txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

        construct_txn = contract.functions["setName"](node, "blockcerts.eth").buildTransaction({
            'from': self.pubkey,
            'nonce': self.w3.eth.getTransactionCount(self.pubkey),
            'gas': 1000000
        })

        signed = self.acct.signTransaction(construct_txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

        name = contract.functions.name(node).call()
        addr = contract.functions.addr(node).call()

        print(f"set contr <{addr}> to name '{name}'")


if __name__ == '__main__':
    ContractDeployer()
