# cert-deployer

This project deploys smart contracts to the ethereum blockchain enabling the
cert-issuer to modify a certificates' or certificate batches' status respectively,
i.e. to issue or revoke, and the cert-verifier to get that status in order to verify
its validity.

Required forked repositories of the original cert-issuer and cert-verifier are linked below.

`https://github.com/flamestro/cert-issuer`

`https://github.com/flamestro/cert-verifier`

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
service constitutes an appropriate option to solve that problem, since the according
assertion of a public key and ens domain could be e.g. stored within the contract
itself so that information does not get lost.

In conclusion, using the cert-deployer, paired with the cert-issuer and -verifier
linked above, restores the natural blockchain guarantees by moving the revocation
and identity administration to the blockchain – i.e. to a smart contract.

## How deploying smart contract works

Potential issuers find our suggested sample contract in the data directory in the
repository which gets first compiled from source and deployed afterwards. This
contracts is, again, just a suggestion and can of course be modified without limiting
the codes functionality – adequate modifications implied and some adjustments of
the cert-issuer and verifier may be required as well.

After deploying the contract, the cert-deployer links the contract to the potential
issuer's ens domain – more specific adds the contracts address to address field
within the ens entry. This input, can of course be changed when deploying another
contract of course, but note that addresses can only be overwritten. A certain ens
domain can only point to one f.e. contract.

Please make sure you enter the right inputs as i.a. connection data names and paths
respectively.

## Setting the deployer up

We highly recommend to use the cert-deployer within a virtual environment! After
activating the virtual environment, please execute:

`$ python setup.py install`

All necessary dependencies will be installed afterwards. Further required are also
the setups of an ethereum wallet (the wallet has to be registered in the ethereum
chain that being intended to be used later) and an according ens domain.

The last step do be executed is completing the configuration within the conf_eth.ini
file and, if desired, adjusting the smart contract.

Summarizing:
1. clone github repo `$ git clone https://github.com/flamestro/cert-deployer.git`
1. install dependencies within virtualenv `$ python setup.py install`
1. add required information incl. paths and connection data in conf_eth.ini
1. deploy smart contract `$ python deploy.py`
