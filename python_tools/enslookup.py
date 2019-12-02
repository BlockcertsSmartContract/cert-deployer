from ens import ENS
from web3 import Web3

#mainnet
w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/4e2720be356542dca2f7dc73481f9fa5"))
ns1 = ENS.fromWeb3(w3)

#ropsten
w4 = Web3(provider = Web3.HTTPProvider("https://ropsten.infura.io/v3/4e2720be356542dca2f7dc73481f9fa5"))
w4.eth.account.privateKeyToAccount('1e0a051bcf681960b44721bc099c0dbd47fd2974c0ae21491155e3c0ee18cc6e')
ns = ENS.fromWeb3(w4, "0x112234455C3a32FD11230C42E7Bccd4A84e02010")

if __name__ == '__main__':
  
  #if w3.net.version !=1:
  #   print("You have to be connected to mainnet")
  
     ensName = input("Insert an Ethereum Name here ")

     #address
     address= ns.address(ensName)
     print(address)
     
     #owner
     owneri= ns.owner(ensName)
     print(owneri)

    # ns.setup_address(input("Insert an Ethereum Name here "))
   
    # if address == "":
    #    print ("The address does not exist!")
    # else : print("Address : "+ns.address(ensName))
   
