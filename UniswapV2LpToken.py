from web3 import Web3
import web3
from web3.middleware import geth_poa_middleware
from ABIs import abiList
from addresses import addresses
from web3Connect import loadWeb3
import web3.exceptions

#---------------------------------------------------------
# Load Web3
#---------------------------------------------------------
w3 = loadWeb3()
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


#---------------------------------------------------------
# CLASS : UniswapV2LPtoken
#   Use to get Quickswap LP token information
#
# FUNCTIONS :
#   __init__(LP_addr)
#   getTokenDecimals()
#   getFactoryAddress()
#   getReserves()
#   getLastK()
#   getName()
#   getToken0()
#   getToken1()
#   getTotalSupply()
#   getPrice0CumulativeLast()
#   getPrice1CumulativeLast()
#   getSymbol()
#---------------------------------------------------------
class UniswapV2LPtoken:

    #-----------------------------------------------------
    # FUNCTION : __init__
    #   Constructor - loads the contract of the input LP
    #   token address.
    #
    # INPUTS :
    #   addr - LP token address
    #
    # OUTPUT :
    #   N/A
    #-----------------------------------------------------
    def __init__(self, LP_addr):
        self.contract = w3.eth.contract(address=LP_addr, abi=abiList["UniswapV2Pair"])
        self.address = LP_addr
    

    #-----------------------------------------------------
    # FUNCTION : getTokenDecimals
    #   Gets decimals of LP token
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   Decimals of LP token
    #-----------------------------------------------------
    def getTokenDecimals(self):
        return self.contract.functions.decimals().call()


    #-----------------------------------------------------
    # FUNCTION : getFactoryAddress
    #   Gets factory address of LP token
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   LP token factory address
    #-----------------------------------------------------
    def getFactoryAddress(self):
        return self.contract.functions.factory().call()


    #-----------------------------------------------------
    # FUNCTION : getReserves
    #   Gets total pool supply of each included ERC20 token
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   [0] - Total pool supply of token 0 (Decimals unadjusted)
    #   [1] - Total pool supply of token 1 (Decimals unadjusted)
    #   [2] - UNIX timestamp
    #-----------------------------------------------------
    def getReserves(self):
        try:
            return self.contract.functions.getReserves().call()
        except web3.exceptions.ContractLogicError:
            return False
        except web3.exceptions.BadFunctionCallOutput:
            return False


    #-----------------------------------------------------
    # FUNCTION : getLastK
    #   Gets current value of 'k'
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   Current value of 'k' (decimals unadjusted)
    #-----------------------------------------------------
    def getLastK(self):
        return self.contract.functions.kLast().call()


    #-----------------------------------------------------
    # FUNCTION : getName
    #   Gets name of LP token
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   Name of LP token
    #-----------------------------------------------------
    def getName(self):
        return self.contract.functions.name().call()


    #-----------------------------------------------------
    # FUNCTION : getToken0
    #   Gets token 0 address
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   Token 0 address
    #-----------------------------------------------------
    def getToken0(self):
        return self.contract.functions.token0().call()


    #-----------------------------------------------------
    # FUNCTION : getToken1
    #   Gets token 1 address
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   Token 1 address
    #-----------------------------------------------------
    def getToken1(self):
        return self.contract.functions.token1().call()


    #-----------------------------------------------------
    # FUNCTION : getTotalSupply
    #   Gets total supply of LP token
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   LP token total supply
    #-----------------------------------------------------
    def getTotalSupply(self):
        return self.contract.functions.totalSupply().call()


    #-----------------------------------------------------
    # FUNCTION : getPrice0CumulativeLast
    #   !!!!
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   !!!!
    #-----------------------------------------------------
    def getPrice0CumulativeLast(self):
        return self.contract.functions.price0CumulativeLast().call()


    #-----------------------------------------------------
    # FUNCTION : getPrice1CumulativeLast
    #   !!!!
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   !!!!
    #-----------------------------------------------------
    def getPrice1CumulativeLast(self):
        return self.contract.functions.price1CumulativeLast().call()


    #-----------------------------------------------------
    # FUNCTION : getSymbol
    #   Gets LP token symbol
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   LP token symbol
    #-----------------------------------------------------
    def getSymbol(self):
        return self.contract.functions.symbol().call()

a = UniswapV2LPtoken(addresses["USDC"])
print(a.getReserves())