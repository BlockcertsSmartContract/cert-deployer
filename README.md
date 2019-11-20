# Extending BlockCerts ethereum backend
to implement on-chain revokation of certificates
and a persistent identity

## dependencies
- truffle framework
- python3 with web3py
- ganache(-cli)

## set up
1. Clone github repo
`$ git clone https://github.com/flamestro/BlockCertsOnchainingEth.git`

2. Start ganache

3. Deploy smart contract to ganache test blockchain
`$ truffle deploy --reset`

4. Run `python_tools/connections.py`
