ENS.
from blockchain_handlers.connectors import MakeW3, ContractConnection
from blockchain_handlers.namehash import namehash
import cert_deployer.config as config



app_config = config.get_config()

w3Factory = MakeW3(app_config)
_w3 = w3Factory.w3
_acct = w3Factory.account
_pubkey = app_config.deploying_address
_ens_name = app_config.ens_name

ens_resolver = ContractConnection("ens_resolver", app_config)

node = namehash("blockcertstest.eth")
addr = ens_resolver.functions.call("addr", node)
name = ens_resolver.functions.call("name", node)

print("before: addr: " + addr)

contr_address = _w3.toChecksumAddress("0xbbca5e794a042e0557222bf284b85a4bc25c2577")
ens_resolver.functions.transact("setAddr", node, contr_address)

addr = ens_resolver.functions.call("addr", node)

print("after: addr: " + addr)

contr_address = _w3.toChecksumAddress("0x0000000000000000000000000000000000000000")
ens_resolver.functions.transact("setAddr", node, contr_address)

addr = ens_resolver.functions.call("addr", node)

print("reset: addr: " + addr)
