import onchaining_tools.path_tools as tools

file_path = tools.get_pk_path()

with open(file_path, "r") as f:
    privateKey = f.read().rstrip('\n')

config = {
    "current_chain": "ropsten",
    "wallets":
        {
            "ropsten":
                {
                    "url": "https://ropsten.infura.io/v3/a70de76e3fd748cbb6dbb2ed49dda183",
                    "privkey": privateKey
                },
            "ganache":
                {
                    "url": "http://localhost:8545",
                    "privkey": privateKey
                }
        }
}
