# cert-deployer

This project deploys smart contracts to the Ethereum blockchain enabling the
cert-issuer to modify a certificates' or certificate batches' status respectively,
i.e. to issue or revoke, and the cert-verifier to get that status in order to verify
its validity.

The related forked repositories of the original cert-issuer and cert-verifier are linked
below.

https://github.com/BlockcertsSmartContract/cert-issuer

https://github.com/BlockcertsSmartContract/cert-verifier

## How deploying smart contract works

Potential issuers find our suggested sample contract in the data directory which
gets, first, compiled from source and, second, deployed afterwards. This contracts is, again,
just a suggestion and can of course be modified without limiting the codes functionality
– adequate modifications implied (note that some adjustments of the cert-issuer and verifier
 may be required as a consequence).

After deploying the contract, the cert-deployer links the contract to the potential
issuer's ENS domain – more specific sets the contract's address as the ENS entry's
address attribute. This input, can, of course, be changed when deploying another
contract, but please note that addresses can only be overwritten, since the ENS
domain can point to only one (contract) address.

## Setting the cert-deployer up

The cert-deployer requires some preparation before it can be used. This preparation
includes certain administrative as well as technical steps to be fulfilled being
explained a bit more in detail below.

### Prerequisites

We highly recommend to use the cert-deployer within a virtual environment! After
activating the virtual environment, please execute:

`$ python setup.py install`

All necessary dependencies will be installed afterwards. Further required are also
the setups of an Ethereum wallet (the wallet has to be registered in the Ethereum
chain that being intended to be used later) and an according ENS domain.

Our recommended tool for creating and managing the wallet is [Metamask](https://metamask.io)
which is, used as its chrome extension, an at least very viable option for an
efficient ENS name registration using the [web application](https://app.ens.domains/). Please make sure that
your wallet has access to a sufficient amount of ether any time.

### Configuring cert-deployer

The last step to be executed is completing the configuration inputs (optional:
adjusting the smart contract). The conf_eth.ini file includes the following parameters:

```
deploying_address = <Your Ethereum address>

chain = <ethereum_ropsten|ethereum_mainnet>
node_url = <ethereum web3 public node url (e.g. infura)>

ens_name = <Your ENS name registered with your ethereum address>
overwrite_ens_link = <Do you want to overwrite a present link to a smart contract? True/False>

usb_name= </Volumes/path-to-usb/>
key_file= <file-you-saved-pk-to>
```

Notes:
1. The ethereum address corresponds to the respective wallet address.
1. Potential issuers can set up their own infura nodes or use publicly shared ones.
1. If a smart contract shall be deployed and used by an already to another contract
linked ENS name, the `overwrite_ens_link` has to be  set to `True` in order to prevent
accidental overwriting.
1. The cert-deployer uses a separate class to access the wallet's private key which
should be stored under the path provided. Ideally, that location is not permanently
accessible (e.g. USB stick) improving security.

### Long story short

Execute these instructions step-by-step:
1. ensure you have installed [solidity compiler (solc)](https://solidity.readthedocs.io/en/v0.5.3/installing-solidity.html)
1. clone github repo `$ git clone https://github.com/BlockcertsSmartContract/cert-deployer.git`
1. install dependencies within virtualenv `$ python setup.py install`
1. add required information incl. paths and connection data into conf_eth.ini
1. deploy smart contract `$ python deploy.py`

... install the forked cert-issuer- (and cert-verifier) repositories for benefitting
from the whole framework (links above).

## Why use cert-deployer

While it is possible to deploy batches to the Ethereum blockchain separately, it
is impossible to modify associated information as e.g. attributes, since the data,
once deployed,is immutable by nature. As certificates could be revoked eventually,
[BlockCerts](https://github.com/blockchain-certificates) has addressed this issue
with external server provided revocation lists. Unfortunately, the cert-verifier's
functionality is, as a consequence, limited by either temporal or permanent offline
times of these servers. Due to its resulting inability distinguishing between valid
and invalid certificates this design destroys especially the processes availability
guarantee naturally coming with the use of blockchains.

In order to restore i.a. the availability guarantee over the entire certificates'
lifetime, we provide an extension of the existing Blockcerts implementation that
issues and revokes certificates using a smart contracts mapping ability, thus making
a certificates' (or batches') status editable after being deployed (excl. for the
issuer).

Another similar issue is the original identity management including the publication
of issuer identities (public keys) on external servers. This is mostly disadvantageous
in case of a permanent server shutdown requiring the public key to have become public
knowledge in the meantime. Otherwise, all future verifications of associated certificates
would become impossible. The usage of the Ethereum name service constitutes an
efficient option solving that problem, since the according assertion of a public
key and ENS domain could be e.g. stored within the contract itself so that this
information does not get lost over time.

In conclusion, using the cert-deployer, paired with the cert-issuer and -verifier
linked above, the natural blockchain guarantees are restored by moving the revocation
and identity administration to the blockchain – i.e. to a smart contract.
