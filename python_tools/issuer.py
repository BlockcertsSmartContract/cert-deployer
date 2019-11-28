<<<<<<< HEAD
from connections import TruffleContract
from cert import Certificate
from compiler import compiling
import random

contract_conn = TruffleContract('http://localhost:8545', '../build/contracts/BlockCertsOnchaining.json')
contract_obj = contract_conn.get_contract_object()

issuer = compiling.compiler(local)

# wrap function calls
def issueCert(merkleRootHash):
	try:
		issuer.functions.issueCert(merkleRootHash).transact()
		print("issued cert with merkleRootHash " + str(merkleRootHash))
	except ValueError:
		print("could not issue cert with merkleRootHash " + str(merkleRootHash) + ". No permission?")
	# except ValidationError:
		# print("wrong arguments")

def revokeCert(merkleRootHash):
	try:
		issuer.functions.revokeCert(merkleRootHash).transact()
		print("issued cert with merkleRootHash " + str(merkleRootHash))
	except ValueError:
		print("could not revoke cert with merkleRootHash " + str(merkleRootHash) + ". No permission?")

def getCertByMRH(index):
	"""get certificate by merkle root hash"""
	try:
		return issuer.functions.certs(index).call()
	except:
		print("Could not get certificate by index: " + str(index) + ". Correct data type?")

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
