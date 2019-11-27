import json
from Web3 import web3 

ganache = false #FLAG --> use of ropsten

issuer = ''#INSERT address with 0x prefix here

smartcontractaddress = ''#insert address with 0x prefix here
data = json.loads('')#insert contract ABI here from remix

contract = new web3.etc.Contract(data, smartcontractaddress)

if(ganache):
	ganache_url = "" #INSERT
	web3 = Web3(Web3.HTTPProvider(ganache_url))

else:
	web3 = Web3('https://ropsten.infura.io/hqRzEqFKv6IsjRxfVUWH')
	privateKeyIssuer = "" #INSERT

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


