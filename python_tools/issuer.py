from connections import TruffleContract
from cert import Certificate
import random

# always accesses last deployed contract instance
contract_conn = TruffleContract('http://localhost:8545', '../build/contracts/BlockCertsOnchaining.json')
contract_obj = contract_conn.get_contract_object()


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
