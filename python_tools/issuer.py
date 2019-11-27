#! /usr/bin/python
from connections import ContractConnection
from compiler import compiling

local = input("Do You Want to Deploy Locally? (True = Local, False = Remote on Ropsten Testnet)\n") #need to have user entering bool if ganache or ropsten

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

issueCert(666)


