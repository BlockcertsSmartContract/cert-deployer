usb_path = "/home/flamestro/"
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
                    "privkey": "7eccfafe502e3bb9ead6b928a0b9403c49c249a64bc7256b0bcfab4d20efef87",
                    "pubkey": "0xb3967C7E984Ea3e391513Fc212843956f33cB6C9"
                }
        }
}
