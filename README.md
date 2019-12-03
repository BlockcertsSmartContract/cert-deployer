# Extending BlockCerts' ethereum backend
to implement on-chain revocation of certificates and a persistent identity using ENS

## dependencies
- python3 with web3py
- ganache
- (optional) python virtualenv

## set up
1. clone github repo `$ git clone https://github.com/flamestro/BlockCertsOnchainingEth.git`
1. install dependencies (see: `requirements.txt`)
1. in `config.py`:
  1. add url and keypair for desired ethereum network
  1. set `current_chain` to reflect your changes
1. (optional) start ganache
1. deploy smart contract `$ deploy.py`

## arguments
- run `python_tools/issuer.py --issue [merkle_root_hash]` to issue
- run `python_tools/issuer.py --revoke [hash]` to revoke a certificate or batch by its hash
- run `python_tools/issuer.py --verifyCert [merkle_root_hash] [cert_hash]` to verify a certificate

## style guides
- PEP8
- tests should be test_whenSomeThing_thenSomeThing
- variables and functions should be all lowercase
- clarify function returns
