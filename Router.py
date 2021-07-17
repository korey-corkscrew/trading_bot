from web3 import Web3
from web3.middleware import geth_poa_middleware
from ABIs import abiList
from addresses import addresses
from UniswapV2Router import UniswapV2Router
from web3Connect import loadWeb3
from ERC20 import ERC20
from AuguryPoolIDs import AuguryPoolIDs
from UniswapV2LpToken import UniswapV2LPtoken

#---------------------------------------------------------
# Load Web3
#---------------------------------------------------------
w3 = loadWeb3()
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


#---------------------------------------------------------
# CLASS : LP_token
#   Wrapper for the other three classes included. Allows
#   user to get information on the LP token and the two tokens
#   used in the pool by only inputting the LP token address.
#
# FUNCTIONS :
#   __init__()
#   
#---------------------------------------------------------
class Router:

    #-----------------------------------------------------
    # FUNCTION : __init__
    #   Constructor - loads the contract of the input LP
    #   token address. Creates instance of Uniswap Router.
    #   
    #
    # INPUTS :
    #   addr - LP token address
    #
    # OUTPUT :
    #   N/A
    #-----------------------------------------------------
    def __init__(self, routerAddr):

        # Load exchange router contract
        self.exchange = UniswapV2Router(routerAddr)


    #-----------------------------------------------------
    # FUNCTION : getLpTokenData
    #   !!
    #
    # INPUTS :
    #   lpAddr - LP token address
    #
    # OUTPUT :
    #   !!
    #-----------------------------------------------------
    def getLpTokenData(self, lpAddr):

        # Load LP token contract
        lpToken = UniswapV2LPtoken(lpAddr)

        # Load token 0 contract
        token0 = ERC20(self.lpToken.getToken0())

        # Load token 1 contract
        token1 = ERC20(self.lpToken.getToken1())


        return {
            "lpToken" : {
                "symbol" : lpToken.getSymbol(),
                "name" : lpToken.getName(),
                "address" : lpToken.address,
                "lastK" : lpToken.getLastK(),
                "decimals" : lpToken.getTokenDecimals(),
                "reserves" : {
                    "token0" : lpToken.getReserves()[0],
                    "token1" : lpToken.getReserves()[1]
                },
                "token0" : {
                    "symbol" : token0.getAllInfo()["symbol"],
                    "name" : token0.getAllInfo()["name"],
                    "address" : token0.getAllInfo()["address"],
                    "decimals" : token0.getAllInfo()["decimals"],
                    "totalSupply" : token0.getAllInfo()["totalSupply"],
                    "priceInUSDC" : self.exchange.getPriceInUSDC(self.token0.tokenAddress)
                },
                "token1" : {
                    "symbol" : token1.getAllInfo()["symbol"],
                    "name" : token1.getAllInfo()["name"],
                    "address" : token1.getAllInfo()["address"],
                    "decimals" : token1.getAllInfo()["decimals"],
                    "totalSupply" : token1.getAllInfo()["totalSupply"],
                    "priceInUSDC" : self.exchange.getPriceInUSDC(self.token1.tokenAddress)
                }
            }
        }


    #-----------------------------------------------------
    # FUNCTION : getPriceInUSDC
    #   !!
    #
    # INPUTS :
    #   tokenAddr - ERC-20 token address
    #
    # OUTPUT :
    #   Market price of (1) input token in USDC
    #-----------------------------------------------------
    def getPriceInUSDC(self, tokenAddr):
        return self.exchange.getPriceInUSDC(tokenAddr)


    #-----------------------------------------------------
    # FUNCTION : swapExact
    #   !!
    #
    # INPUTS :
    #   !!
    #
    # OUTPUT :
    #   !!
    #-----------------------------------------------------
    def swapExact(self, amountIn, fromToken, toToken):

        # Swap token for same token - do nothing
        if(fromToken == toToken):
            return False

        # Swap MATIC for tokens
        elif(fromToken == addresses["MATIC"]):
            return self.exchange.swapExactETHForTokens(amountIn, toToken)

        # Swap tokens to MATIC
        elif(toToken == addresses["MATIC"]):
            return self.exchange.swapExactTokensForETH(amountIn, fromToken)

        # Swap tokens for tokens
        else:
            return self.exchange.swapExactTokensForTokens(amountIn, fromToken, toToken)


    #-----------------------------------------------------
    # FUNCTION : swapForExact
    #   !!
    #
    # INPUTS :
    #   !!
    #
    # OUTPUT :
    #   !!
    #-----------------------------------------------------
    def swapForExact(self, amountOut, fromToken, toToken):

        # Swap token for same token - do nothing
        if(fromToken == toToken):
            return False

        # Swap MATIC for tokens
        elif(fromToken == addresses["MATIC"]):
            return self.exchange.swapETHForExactTokens(amountOut, toToken)

        # Swap tokens to MATIC
        elif(toToken == addresses["MATIC"]):
            return self.exchange.swapTokensForExactETH(amountOut, fromToken)

        # Swap tokens for tokens
        else:
            return self.exchange.swapTokensForExactTokens(amountOut, fromToken, toToken)

    '''
    def getPriceImpact(self, amountIn, fromToken, toToken):
        #FIXME: Find way to get lp address by inputting 2 token addresses
        lpAddr = 0

        lpToken = UniswapV2LPtoken(lpAddr)
        if(lpToken.getToken0 == fromToken):
            newFromTokenPoolAmount = amountIn + lpToken.getReserves()[0]
            newToTokenPoolAmount = lpToken.getLastK() / newFromTokenPoolAmount
            toTokenReceived = lpToken.getReserves()[1] - newToTokenPoolAmount
            toTokenPer
    '''