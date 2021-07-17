from web3 import Web3
from web3.middleware import geth_poa_middleware


#---------------------------------------------------------
# Load Web3
#---------------------------------------------------------
def loadWeb3():
    return Web3(Web3.HTTPProvider('https://rpc-mainnet.maticvigil.com/v1/67ee67f1d107231cfb13bd5e672685c15ed151c8'))