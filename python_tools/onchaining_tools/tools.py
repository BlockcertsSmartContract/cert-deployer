import os


# returns the path to the project root dir

def get_root_dir() -> str:
    root_dir = os.path.abspath(__file__)
    for _ in range(3):
        root_dir = os.path.dirname(root_dir)
    return root_dir


# always accesses last deployed contract instance

def get_contract_as_json_path() -> str:
    return get_root_dir() + '/build/contracts/BlockCertsOnchaining.json'


def get_contract_path() -> str:
    return get_root_dir() + "/contracts/BlockCertsOnchaining.sol"


def get_config_data_path() -> str:
    return get_root_dir() + "/data/compile_opt.json"


def get_host() -> str:
    return 'http://localhost:8545'
