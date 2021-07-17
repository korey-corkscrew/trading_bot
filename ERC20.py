from web3 import Web3
from web3.middleware import geth_poa_middleware
from ABIs import abiList
from web3Connect import loadWeb3

#---------------------------------------------------------
# Load Web3
#---------------------------------------------------------
w3 = loadWeb3()
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

#---------------------------------------------------------
# CLASS : ERC20
#   Use to get basic information about any ERC20 token
#
# FUNCTIONS :
#   __init__(addr)
#   getName()
#   getDecimals()
#   getTotalSupply()
#   getBalanceOf(addr)
#   getAllInfo()
#---------------------------------------------------------
class ERC20:

    #-----------------------------------------------------
    # FUNCTION : __init__
    #   Constructor - loads the contract of the input ERC20
    #   token address.
    #
    # INPUTS :
    #   addr - ERC20 token address
    #
    # OUTPUT :
    #   N/A
    #-----------------------------------------------------
    def __init__(self, addr):
        self.contract = w3.eth.contract(address=addr, abi=abiList["ERC20"])
        self.tokenAddress = addr


    #-----------------------------------------------------
    # FUNCTION : getName
    #   Gets the ERC20 token name.
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   ERC20 token name
    #-----------------------------------------------------
    def getName(self):
        return self.contract.functions.name().call()


    #-----------------------------------------------------
    # FUNCTION : getDecimals
    #   Gets the number of decimals the ERC20 token has.
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   Number of ERC20 token decimals
    #-----------------------------------------------------
    def getDecimals(self):
        return self.contract.functions.decimals().call()


    #-----------------------------------------------------
    # FUNCTION : getSymbol
    #   Gets the symbol of the ERC20 token.
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   Symbol of the ERC20 token
    #-----------------------------------------------------
    def getSymbol(self):
        return self.contract.functions.symbol().call()


    #-----------------------------------------------------
    # FUNCTION : getTotalSupply
    #   Gets the total supply the ERC20 token has.
    #   Leaves value as it is returned. Decimals are adjusted.
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   Total supply of the ERC20 token
    #-----------------------------------------------------
    def getTotalSupply(self):
        return self.contract.functions.totalSupply().call()


    #-----------------------------------------------------
    # FUNCTION : getBalanceOf
    #   Gets the current balance of ERC20 token in the 
    #   input address. (Use to see the pool supply for
    #   individual tokens)
    #
    # INPUTS :
    #   address - Address wanting to find balance of
    #
    # OUTPUT :
    #   Current balance of ERC20 token in input address
    #-----------------------------------------------------
    def getBalanceOf(self, address):
        return self.contract.functions.balanceOf(address).call()


    #-----------------------------------------------------
    # FUNCTION : getAllInfo
    #   Returns general information of any ERC-20 token.
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   ERC-20 token information
    #-----------------------------------------------------
    def getAllInfo(self):
        return {
            "symbol" : self.getSymbol(), 
            "name" : self.getName(), 
            "totalSupply" : self.getTotalSupply(),
            "decimals" : self.getDecimals(),
            "address" : self.tokenAddress
        }