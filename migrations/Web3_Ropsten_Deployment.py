import json
from Web3 import web3 

Tx = require ('ethereum-tx')
Web3 = require('web3')
web3 = new Web3('https://ropsten.infura.io/hqRzEqFKv6IsjRxfVUWH')

issuer = ''#insert address with 0x prefix here
#recipient = ''#same

smartcontractaddress = ''#insert address with 0x prefix here
data = ''#insert contract ABI here from remix

contract = new web3.etc.Contract(data, smartcontractaddress)

privateKeyIssuer = Buffer.from(process.env.PRIVATE_KEY_ISSUER, 'hex')

web3.eth.getTransactionCount(issuer, (err, txCount) => {

	const txObject = {
		nonce: web3.utils.toHex(txCount), 
		gasLimit: web3.utils.toHex(8000),#have to insert amount x here
		gasPrice: web3.utils.toHex(web3.utils.toWei('10', 'gwei')),#have to insert amount x here
		to: smartcontractaddress,
		data: contract.methods.X(argument).encodeABI() #call function X with respective parameters. look up available (external) functions in remix too
	}

	const tx = new Tx(txObject)
	tx.sign(privateKeyIssuer)

	const serializedTx = tx.serialize()
	const raw = '0x' + serializedTx.toString('hex')

	web3.eth.sendSignedTransaction(raw, (err, txHash) => {
		console.log('err: ', err, ', Transaction Hash: ' + txHash)
	})
})