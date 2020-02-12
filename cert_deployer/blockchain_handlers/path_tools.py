import os


def get_root_dir():
    root_dir = os.path.abspath(__file__)
    for _ in range(3):
        root_dir = os.path.dirname(root_dir)
    return root_dir

def get_contr_path():
    return get_root_dir() + "/contracts/CertificateStore.sol"

def get_contr_info_path():
    return get_root_dir() + "/data/contr_info.json"

def get_compile_data_path():
    return get_root_dir() + "/data/compile_opt.json"
