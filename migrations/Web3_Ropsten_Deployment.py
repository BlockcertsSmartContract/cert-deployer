import json
from Web3 import web3 

#if using ganache
#ganache_url = "" #insert ganache url
#web3 = Web3(Web3.HTTPProvider(ganache_url))

#if using ropsten infura node 
Web3 = require('web3')
web3 = Web3('https://ropsten.infura.io/hqRzEqFKv6IsjRxfVUWH')

issuer = ''#insert address with 0x prefix here

smartcontractaddress = ''#insert address with 0x prefix here
data = ''#insert contract ABI here from remix

contract = new web3.etc.Contract(data, smartcontractaddress)

privateKeyIssuer = ""#insert key here

nonce = web3.eth.getTransactionCount(issuer)

txObject = {
	nonce: nonce, 
	gasLimit: web3.toHex(8000),#have to insert amount x here
	gasPrice: web3.toHex(web3.toWei('10', 'gwei')),#have to insert amount x here
	to: smartcontractaddress,
	data: contract.methods.X(argument).encodeABI() #call function X with respective parameters. look up available (external) functions in remix too
}

tx = web3.eth.account.signTransaction(txObject, privateKeyIssuer)
tx_hash = web3.eth.sendRawTransaction(tx.rawTransaction)

print(web3.toHex(tx_hash))

