# Extending BlockCerts' ethereum backend
to implement on-chain revokation of certificates and a persistent identity

## dependencies
- truffle framework
- python3 with web3py
- ganache(-cli)
- (optional) python virtualenv

## set up
1. Clone github repo `$ git clone https://github.com/flamestro/BlockCertsOnchainingEth.git`
2. Start ganache
3. Deploy smart contract `$ deploy.py`

## arguments
- Run `python_tools/issuer.py --issue someBatchHash someCertHash` to issue
- Run `python_tools/issuer.py --revokeCert someBatchHash someCertHash` to revoke a certificate
- Run `python_tools/issuer.py --revokeBatch someBatchHash someCertHash` to revoke a batch
- Run `python_tools/issuer.py --verifyCert someBatchHash someCertHash` to verify a certificate

## style guides
- PEP8
- Tests should be test_whenSomeThing_thenSomeThing
- variables and functions should be all lowercase 
- clarify function returns
