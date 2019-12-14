import argparse
import json

import content_hash
import ipfshttpclient
import onchaining_tools.config as config
import onchaining_tools.path_tools as tools
from ens import ENS
from onchaining_tools.connections import MakeW3, ContractConnection
from solc import compile_standard


class ContractDeployer(object):
    ''' Compiles, signes and deploys a smart contract on the ethereum blockchain
    Args:
        object(web3 object): instantiated web3 connection to ethereum node
            print("cat : " + str(client.cat(res['Hash'])))
    '''

    def __init__(self):
        '''Defines blockchain, initializes ethereum wallet, calls out compilation and deployment functions'''
        try:
            self._client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
            print("connected to IPFS")
        except:
            print("Not connected to IPFS -> start daemon to deploy contract info on IPFS")
            self._client = None
        current_chain = config.config["current_chain"]
        w3Factory = MakeW3()
        self.w3 = w3Factory.get_w3_obj()
        self.acct = w3Factory.get_w3_wallet()
        self.pubkey = self.acct.address
        self.compile_contract()
        self.deploy()
        self.ipfs_hash = ""
        if self._client is not None:
            self.ipfs_hash = self._client.add(tools.get_contr_info_path())['Hash']
            print("IPFS Hash is :" + self.ipfs_hash)
            print("You can check the abi on: https://ipfs.io/ipfs/" + self.ipfs_hash)
            print("You can check the abi on: ipfs://" + self.ipfs_hash)
        if current_chain == "ropsten":
            self.assign_ens()
        if self._client is not None:
            self._client.close()

    def compile_contract(self):
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

    def deploy(self):
        '''Signes raw transaction and deploys it on the blockchain'''
        contract = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)

        # defining blockchain and public key of the ethereum wallet
        current_chain = config.config["current_chain"]
        acct_addr = self.pubkey

        # building raw transaction
        estimated_gas = contract.constructor().estimateGas()
        print("Estimated gas: ", estimated_gas)
        construct_txn = contract.constructor().buildTransaction({
            'nonce': self.w3.eth.getTransactionCount(acct_addr),
            'gas': estimated_gas
        })

        # signing & sending a signed transaction, saving transaction hash
        signed = self.acct.sign_transaction(construct_txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        print("Gas used: ", tx_receipt.gasUsed)

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
        print(f"deployed contr <{self.contr_address}>")

    def assign_ens(self):
        ens_domain = "blockcerts.eth"
        ens_resolver = ContractConnection("ropsten_ens_resolver")

        self.contr_address = self.w3.toChecksumAddress(self.contr_address)

        ns = ENS.fromWeb3(self.w3)
        node = ns.namehash(ens_domain)
        codec = 'ipfs-ns'

        ens_resolver.functions.transact("setAddr", node, self.contr_address)
        ens_resolver.functions.transact("setName", node, ens_domain)
        if self._client is not None:
            chash = content_hash.encode(codec, self.ipfs_hash)
            ens_resolver.functions.transact("setContenthash", node, chash)

        addr = ens_resolver.functions.call("addr", node)
        name = ens_resolver.functions.call("name", node)

        content = "that is empty"
        if self._client is not None:
            content = (ens_resolver.functions.call("contenthash", node)).hex()
            content = content_hash.decode(content)

        print(f"set contr <{addr}> to name '{name}' with content '{content}'")
        

if __name__ == '__main__':
    '''Parses arguments and calls out respective functionatilites.
        Args: [ropsten/ganache] 
    '''
    parser = argparse.ArgumentParser()
    # args: deploy local or remote
    parser.add_argument("provider", help="supported providers are ropsten and ganache", type=str)
    arguments = parser.parse_args()
    if arguments.provider == "ropsten":
        try:
            config.config["current_chain"] = "ropsten"
            print("Deploying contract on ropsten")
            ContractDeployer()
        except ValueError as e:
            print("Something went wrong :", e)
    elif arguments.provider == "ganache":
        try:
            config.config["current_chain"] = "ganache"
            print("Deploying contract on ganache")
            ContractDeployer()
        except ValueError as e:
            print("Something went wrong :", e)
    else:
        print("Please choose ropsten or ganache as provider")
