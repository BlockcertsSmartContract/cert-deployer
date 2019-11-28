from connections import TruffleContract
from cert import Certificate
from compiler import compile_contract
import random

contract_conn = TruffleContract('http://localhost:8545', '../build/contracts/BlockCertsOnchaining.json')

# contract_obj = contract_conn.get_contract_object()
contract_obj = compile_contract(contract_conn.w3)
# print(contract_obj.accounts)

c1 = Certificate(random.randint(100, 999), random.randint(100, 999), contract_obj)


print("issue batch")
c1.issue()
c1.isCertValid()
print()
print("revoke cert")
c1.revokeCert()
c1.isCertValid()
print()
print("revoke batch")
c1.revokeBatch()
c1.isCertValid()
