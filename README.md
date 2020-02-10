# cert-deployer

This project deploys smart contracts to the ethereum blockchain enabling the
cert-issuer to modify a certificates' or certificate batches' status respectively,
i.e. to issue or revoke, and the cert-verifier to get that status in order to verify
its validity.

Required forked repositories of the original cert-isser and cert-verifier are linked below.

https://github.com/flamestro/cert-issuer
https://github.com/flamestro/cert-verifier

## Why using cert-deployer

While it is possible to deploy batches to the ethereum chain separately, it is
impossible to modify related data as e.g. attributes, since data, once deployed
to the blockchain, is immutable by nature. As certificates' states could be
revoked eventually after the deployment, BlockCerts v2 has addressed this issue
with external server provided revocation lists. Unfortunately, the cert-verifier's
functionality is determined by over either temporal or long-term offline times
these servers, due to its inability distinguishing between valid and invalid
certificates – thus destroying especially the availability guarantee that naturally
come with the use of blockchains.

In order to restore i.a. the availability guarantee over the entire certificates'
lifetime of we provide an extension of the existing Blockcerts implementation that
issues and revokes certificates using a smart contracts mapping ability thus making
a certificates' (or batches') status editable after being deployed (excl. for the
issuer).

Another similar issue is the original identity management including the publication
of the issuer's identity (public key) on an external server as well. This is mostly
disadvantageous in case of permanent server shutdown requiring the public key to
have become public knowledge in the meantime. Otherwise, all future verifications
of according certificates would become impossible. The usage of the ethereum name
system constitutes an appropriate option to solve that problem, since the according
assertion of a public key and ens domain could be e.g. stored within the contract
itself so that information does not get lost.

In conclusion, using the cert-deployer, paired with the cert-issuer and -verifier
linked above, restores the natural blockchain guarantees by moving the revocation
and identity administration to the blockchain – i.e. to a smart contract.


## How deploying smart contract works


# Extending BlockCerts' ethereum backend
to implement on-chain revocation of certificates and a persistent identity using ENS

## dependencies
- python3 with web3py
- ganache
- (optional) python virtualenv
- (optional) ipfs daemon

## set up
1. (optional) To have decentralization of contract info you have to run ipfs daemon locally while using this tool
1. clone github repo `$ git clone https://github.com/flamestro/BlockCertsOnchainingEth.git`
1. install dependencies (see: `requirements.txt`)
1. in `config.py`:
  1. add url and keypair for desired ethereum network
  1. set `current_chain` to reflect your changes
1. (optional) start ganache
1. deploy smart contract `$ deploy.py`

## arguments
- run `python_tools/issuer.py -h` to get descriptions

## style guides
- PEP8
- tests should be test_whenSomeThing_thenSomeThing
- variables and functions should be all lowercase
