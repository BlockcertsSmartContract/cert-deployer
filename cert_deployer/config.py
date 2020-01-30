import logging
import os

import configargparse

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG = None


def configure_logger():
    # Configure logging settings; create console handler and set level to info
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


# restructured arguments to put the chain specific arguments together.
def add_arguments(p):
    p.add('-c', '--my-config', required=False, env_var='CONFIG_FILE',
          is_config_file=True, help='config file path')
    p.add_argument('--deploying_address', required=True, help='deploying address', env_var='DEPLOYING_ADDRESS')
    p.add_argument('--node_url', required=True, help='issuing node (infura)', env_var='NODE_URL')
    p.add_argument('--ens_name', required=True, help='ENS domain', env_var='ENS_NAME')
    p.add_argument('--usb_name', required=True, help='usb path to key_file', env_var='USB_NAME')
    p.add_argument('--key_file', required=True, help='name of file on USB containing private key', env_var='KEY_FILE')
    p.add_argument('--max_retry', default=10, type=int, help='Maximum attempts to retry transaction on failure', env_var='MAX_RETRY')
    p.add_argument('--overwrite_ens', default=False, type=bool, help='Should a linked contract be overwritten?', env_var='OVERWRITE_ENS')
    p.add_argument('--chain', default='ethereum_ropsten',
                   help=('Which chain to use. Default is ethereum_ropsten. Other option is ethereum_mainnet'), env_var='CHAIN')
    p.add_argument('--safe_mode', dest='safe_mode', default=True, action='store_true',
                   help='Used to make sure your private key is not plugged in with the wifi.', env_var='SAFE_MODE')
    p.add_argument('--no_safe_mode', dest='safe_mode', default=False, action='store_false',
                   help='Turns off safe mode. Only change this option for testing or unit testing.', env_var='NO_SAFE_MODE')


def get_config():

    configure_logger()
    p = configargparse.getArgumentParser(default_config_files=[os.path.join(PATH, 'conf_ethtest.ini'),
                                                                'conf_ethtest.ini'])
    add_arguments(p)
    parsed_config, _ = p.parse_known_args()

    if not parsed_config.safe_mode:
        logging.warning('Your app is configured to skip the wifi check when the USB is plugged in. Read the '
                        'documentation to ensure this is what you want, since this is less secure')

    logging.info('This run will try to issue on the %s chain', parsed_config.chain)

    global CONFIG
    CONFIG = parsed_config
    return parsed_config
