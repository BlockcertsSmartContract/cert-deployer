import os


def get_root_dir() -> str:
    root_dir = os.path.abspath(__file__)
    for _ in range(3):
        root_dir = os.path.dirname(root_dir)
    return root_dir


def get_contract_path() -> str:
    return get_root_dir() + "/contracts/BlockCertsOnchaining.sol"


def get_compile_data_path() -> str:
    return get_root_dir() + "/data/compile_opt.json"


def get_contr_info_path() -> str:
    return get_root_dir() + "/data/contr_info.json"


def get_ens_abi_path() -> str:
    return get_root_dir() + "/data/ens_abi.json"
