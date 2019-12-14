usb_path = "your/usb/path"
pk_file = "pk.txt"

privateKey = open(usb_path + pk_file, "r").read()

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
