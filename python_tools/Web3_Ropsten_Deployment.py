import json
from Web3 import web3 

ganache = false #FLAG --> use of ropsten

issuer = ''#INSERT address with 0x prefix here
privateKeyIssuer = "" #INSERT

smartcontractaddress = ''#insert address with 0x prefix here
data = json.loads('')#insert contract ABI here from remix

contract = new web3.etc.Contract(data, smartcontractaddress)

nodeurl = 'https://ropsten.infura.io/hqRzEqFKv6IsjRxfVUWH'

if(ganache):
	nodeurl = 'http://localhost:8545' #INSERT

elif(!ganache):
	privateKeyIssuer = "" #INSERT, we only need this key if locked non-ganache account
	
web3 = Web3(nodeurl)
nonce = web3.eth.getTransactionCount(issuer)

txObject = {
	nonce: nonce, 
	gasLimit: web3.toHex(8000), #INSERT
	gasPrice: web3.toHex(web3.toWei('10', 'gwei')), #INSERT
	to: smartcontractaddress,
	data: contract.methods.X(argument).encodeABI() #call function X with respective parameters. look up available (external) functions in remix too
}


if (ganache == false): #only need to sign if we want to access to ropsten with locked account
	tx = web3.eth.account.signTransaction(txObject, privateKeyIssuer)

tx_hash = web3.eth.sendRawTransaction(tx.rawTransaction)

print(web3.toHex(tx_hash))

#USUEFUL:
	#web3.personal.lockAccount('0xE0ca...c1f7')
	#web3.personal.unlockAccount('0xE0ca...c1f7', 'mypass')


