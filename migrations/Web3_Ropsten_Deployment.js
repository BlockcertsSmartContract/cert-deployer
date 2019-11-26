const argument = "anything"//any argument we want to later use in the function call below

var Tx = require ('ethereum-tx')
const Web3 = require('web3')
const web3 = new Web3('https://ropsten.infura.io/hqRzEqFKv6IsjRxfVUWH')

const issuer = ''//insert address with 0x prefix here
const recipient = ''//same

const smartcontractaddress = ''//insert address with 0x prefix here
const data = ''//insert contract ABI here from remix

const contract = new web3.etc.Contract(data, smartcontractaddress)

const privateKeyIssuer = Buffer.from(process.env.PRIVATE_KEY_ISSUER, 'hex')

web3.eth.getTransactionCount(issuer, (err, txCount) => {

	const txObject = {
		nonce: web3.utils.toHex(txCount), 
		gasLimit: web3.utils.toHex(),//have to insert amount x here
		gasPrice: web3.utils.toHex(web3.utils.toWei('', 'gwei')),//have to insert amount x here
		to: smartcontractaddress,
		data: contract.methods.X(argument).encodeABI()//call function X with respective parameters. look up available (external) functions in remix too
	}

	const tx = new Tx(txObject)
	tx.sign(privateKeyIssuer)

	const serializedTx = tx.serialize()
	const raw = '0x' + serializedTx.toString('hex')

	web3.eth.sendSignedTransaction(raw, (err, txHash) => {
		console.log('err: ', err, ', Transaction Hash: ' + txHash)
	})
})
