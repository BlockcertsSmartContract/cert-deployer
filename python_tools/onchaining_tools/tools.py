import os


def get_root_dir() -> str:
    root_dir = os.path.abspath(__file__)
    for _ in range(3):
        root_dir = os.path.dirname(root_dir)
    return root_dir
