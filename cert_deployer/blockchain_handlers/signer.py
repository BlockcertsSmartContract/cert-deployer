from web3 import Web3, HTTPProvider
import os
import logging

def get_secret(parsed_config):
    '''
    Provides priv key access
    '''
    path_to_secret = os.path.join(parsed_config.usb_name, parsed_config.key_file)

    with open(path_to_secret) as key_file:
        key = key_file.read().strip()

    return key

def sign_transaction(parsed_config, transaction_to_sign):
    # try to sign the transaction.
    wif = get_secret(parsed_config)
    w3 = Web3(HTTPProvider())
    acct = w3.eth.account.from_key(wif)

    signed_tx = acct.sign_transaction(transaction_to_sign)
    return signed_tx
