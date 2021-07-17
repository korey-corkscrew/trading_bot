#from Router import Router
from web3 import Web3
import web3
from web3.middleware import geth_poa_middleware
from web3.types import TxReceipt
from ABIs import abiList
from addresses import addresses
from web3Connect import loadWeb3
import time
from ERC20 import ERC20
from wallet import wallet
import json
from UniswapV2LpToken import UniswapV2LPtoken


#---------------------------------------------------------
# Get user wallet information
#---------------------------------------------------------
userWallet = wallet()

#---------------------------------------------------------
# Load Web3
#---------------------------------------------------------
w3 = loadWeb3()
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


#---------------------------------------------------------
# CLASS : UniswapV2Router
#   Use to get market prices, perform token swaps, and
#   stake/unstake in liquidity pools on exchanges that use 
#   Uniswap V2 router.
#
# FUNCTIONS :
#   __init__()
#   getFactory()
#   getAmountsIn(amoutnOut, *path)
#   getAmountsOut(amountIn, *path)
#   swapETHForExactTokens(amountOut, toToken)
#   swapExactETHForTokens(amountIn, toToken)
#   swapExactTokensForETH(amountIn, fromToken)
#   swapTokensForExactETH(amountOut, fromToken)
#   swapTokensForExactTokens(amountOut, fromToken, toToken)
#   swapExactTokensForTokens(amountIn, fromToken, toToken)
#   getPriceInUSDC(tokenAddr)
#---------------------------------------------------------
class UniswapV2Router:

    #-----------------------------------------------------
    # FUNCTION : __init__
    #   Loads the Uniswap V2 router contract.
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   N/A
    #-----------------------------------------------------
    def __init__(self, routerAddr):
        self.contract = w3.eth.contract(address=routerAddr, abi=abiList["UniswapV2Router"])


    #-----------------------------------------------------
    # FUNCTION : getFactory
    #   Gets the Uniswap V2 factory address.
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   Factory address
    #-----------------------------------------------------
    def getFactory(self):
        return self.contract.functions.factory().call()


    #-----------------------------------------------------
    # FUNCTION : getAmountsIn
    #   Gets the input amounts of numerous tokens relative to 
    #   an exact output amount of a token
    #
    # INPUTS :
    #   amountOut - Number of output tokens
    #   path - List of token addresses [inputTokenA, inputTokenB, ..., outputToken]
    #
    # OUTPUT :
    #   Number of input tokens needed to swap output token 
    #-----------------------------------------------------
    def getAmountsIn(self, amountOut, *path):
        return self.contract.functions.getAmountsIn(amountOut, *path).call()


    #-----------------------------------------------------
    # FUNCTION : getAmountsOut
    #   Gets the output amounts of numerous tokens relative to 
    #   an exact input amount of a token
    #
    # INPUTS :
    #   amountIn - Number of input tokens
    #   path - List of token addresses [inputToken, outputTokenA, outputTokenB, ...]
    #
    # OUTPUT :
    #   Number of output tokens received from swap with input token
    #-----------------------------------------------------
    def getAmountsOut(self, amountIn, *path):
        try:
            return self.contract.functions.getAmountsOut(amountIn, *path).call()
        except web3.exceptions.ContractLogicError:
            return None


    #-----------------------------------------------------
    # FUNCTION : swapETHForExactTokens
    #   Swaps MATIC for an exact amount of tokens
    #
    # INPUTS :
    #   amountOut - Amount of tokens to receive from trade
    #   toToken - Address of token to receive from trade
    #
    # OUTPUT :
    #   Transaction receipt

    # FIXME: Remove logic for adjusting decimals. Leave values as they are received
    #-----------------------------------------------------
    def swapETHForExactTokens(self, amountOut, toToken):

        # Create path (MATIC -> token)
        path = [addresses["MATIC"], toToken]

        # Adjust decimals for out amount
        to_token = ERC20(toToken)
        _amountOut = amountOut * pow(10, to_token.getDecimals())

        # Calculate amount of MATIC for swap
        amountIn = self.getAmountsIn(int(_amountOut), path)[0]

        # 0.5% slippage
        amountInMax = amountIn * 1.05

        userWallet.txParams["value"] = int(amountInMax)

        # Call contract function
        function = self.contract.functions.swapETHForExactTokens(
            int(_amountOut), path, userWallet.address, userWallet.getDeadline()
        )
        return userWallet.processTransaction(function)


    #-----------------------------------------------------
    # FUNCTION : swapExactETHForTokens
    #   Swaps an exact amount of MATIC for tokens
    #
    # INPUTS :
    #   amountIn - Amount of MATIC wanting to trade
    #   toToken - Address of token to receive from trade
    #
    # OUTPUT :
    #   Transaction receipt

    # FIXME: Remove logic for adjusting decimals. Leave values as they are received
    #-----------------------------------------------------
    def swapExactETHForTokens(self, amountIn, toToken):

        # Create path (MATIC -> token)
        path = [addresses["MATIC"], toToken]

        # Get MATIC decimals & adjust amount in
        MATIC = ERC20(addresses["MATIC"])
        amountIn = amountIn * pow(10, MATIC.getDecimals())

        # Amount of MATIC for trade is set as "value"
        # in the transaction parameters
        userWallet.txParams["value"] = int(amountIn)

        # Calculate amount of token for swap
        amountOut = self.getAmountsOut(int(amountIn), path)[-1]

        # 0.5% slippage
        amountOutMin = amountOut - (amountOut * 0.05)

        # Call contract function
        function = self.contract.functions.swapExactETHForTokens(
            int(amountOutMin), path, userWallet.address, userWallet.getDeadline()
        )

        return userWallet.processTransaction(function)


    #-----------------------------------------------------
    # FUNCTION : swapExactTokensForETH
    #   Swaps an exact amount of tokens for MATIC
    #
    # INPUTS :
    #   amountIn - Number of tokens wanting to trade
    #   fromToken - Address of token to trade
    #
    # OUTPUT :
    #   Transaction receipt

    # FIXME: Remove logic for adjusting decimals. Leave values as they are received
    #-----------------------------------------------------
    def swapExactTokensForETH(self, amountIn, fromToken):

        # Create path (token -> MATIC)
        path = [fromToken, addresses["MATIC"]]

        from_token = ERC20(fromToken)
        amountIn = amountIn * pow(10, from_token.getDecimals())

        # Calculate amount of MATIC for swap
        amountOut = self.getAmountsOut(int(amountIn), path)[1]

        # 0.5% slippage
        amountOutMin = amountOut - (amountOut * 0.05)

        # Call contract function
        function = self.contract.functions.swapExactTokensForETH(
            int(amountIn), int(amountOutMin), path, userWallet.address, userWallet.getDeadline()
        )

        return userWallet.processTransaction(function)


    #-----------------------------------------------------
    # FUNCTION : swapTokensForExactETH
    #   Swaps tokens for an exact amount of MATIC
    #
    # INPUTS :
    #   amountOut - Amount of MATIC receiving from trade
    #   fromToken - Address of token to trade
    #
    # OUTPUT :
    #   Transaction receipt

    # FIXME: Remove logic for adjusting decimals. Leave values as they are received
    #-----------------------------------------------------
    def swapTokensForExactETH(self, amountOut, fromToken):

        # Create path (token -> MATIC)
        path = [fromToken, addresses["MATIC"]]

        MATIC = ERC20(addresses["MATIC"])
        amountOut = amountOut * pow(10, MATIC.getDecimals())

        # Calculate amount of MATIC for swap
        amountIn = self.getAmountsIn(int(amountOut), path)[0]

        # 0.5% slippage
        amountInMax = amountIn * 1.05

        # Call contract function
        function = self.contract.functions.swapTokensForExactETH(
            int(amountOut), int(amountInMax), path, userWallet.address, userWallet.getDeadline()
        )
        
        return userWallet.processTransaction(function)


    #-----------------------------------------------------
    # FUNCTION : swapTokensForExactTokens
    #   Swaps token 'A' for an exact amount of token 'B'
    #
    # INPUTS :
    #   amountOut - Number of tokens wanting to receive from trade
    #   fromToken - Address of token giving to trade
    #   toToken - Address of token receiving from trade
    #
    # OUTPUT :
    #   Transaction receipt

    # FIXME: Remove logic for adjusting decimals. Leave values as they are received
    #-----------------------------------------------------
    def swapTokensForExactTokens(self, amountOut, fromToken, toToken):

        # Create path (tokenA -> tokenB)
        path = [fromToken, addresses["MATIC"], toToken]
        _path = [fromToken, toToken]

        to_token = ERC20(toToken)
        amountOut = amountOut * pow(10, to_token.getDecimals())

        # Calculate amount of tokenA for swap
        amountIn = self.getAmountsIn(int(amountOut), path)[0]

        # Calculate amount of tokenA for swap
        _amountIn = self.getAmountsIn(int(amountOut), _path)[0]

        if(amountIn < _amountIn):
            path_ = path
        else:
            path_ = _path

        # 0.5% slippage
        amountInMax = amountIn * 1.05

        # Call contract function
        function = self.contract.functions.swapTokensForExactTokens(
            int(amountOut), int(amountInMax), path_, userWallet.address, userWallet.getDeadline()
        )
        
        return userWallet.processTransaction(function)


    #-----------------------------------------------------
    # FUNCTION : swapExactTokensForTokens
    #   Swaps an exact amount of token 'A' for token 'B'
    #
    # INPUTS :
    #   amountIn - Number of tokens wanting to trade
    #   fromToken - Address of token giving to trade
    #   toToken - Address of token receiving from trade
    #
    # OUTPUT :
    #   Transaction receipt
    #-----------------------------------------------------
    def swapExactTokensForTokens(self, amountIn, fromToken, toToken):

        # Create path (tokenA -> tokenB)
        path = [fromToken, addresses["MATIC"], toToken]
        _path = [fromToken, toToken]

        # Calculate amount of MATIC for swap
        amountOut = self.getAmountsOut(int(amountIn), path)[-1]

        # Calculate amount of MATIC for swap
        _amountOut = self.getAmountsOut(int(amountIn), _path)[-1]

        # Find path with greatest output amount
        if(amountOut > _amountOut):
            path_ = path
        else:
            path_ = _path

        # 0.5% slippage
        amountOutMin = amountOut - (amountOut * 0.05)

        # Call contract function
        function = self.contract.functions.swapExactTokensForTokens(
            int(amountIn), int(amountOutMin), path_, userWallet.address, userWallet.getDeadline()
        )
        
        return userWallet.processTransaction(function)


    #-----------------------------------------------------
    # FUNCTION : getPriceInUSDC
    #   Gets the current market price of ERC20 token (in USDC).
    #
    # INPUTS :
    #   tokenAddr - ERC20 token address
    #
    # OUTPUT :
    #   Current token market price in USDC
    #-----------------------------------------------------
    def getPriceInUSDC(self, tokenAddr):

        token = ERC20(tokenAddr)

        # Check if token 0 is USDC
        if(tokenAddr == addresses["USDC"]):
            
            # Token 0 is USDC - Set price to $1.00
            tokenPriceInUSDC = 1.00

        # Token 0 is not USDC
        else:

            # Get token 0 market price in USDC
            tokenPrice = self.getAmountsOut(1 * pow(10, token.getDecimals()), [tokenAddr, addresses["USDC"]])
            if(tokenPrice == None):
                return None
            
            # Adjust decimals
            tokenPriceInUSDC = tokenPrice[1] * pow(10, -6)

        return tokenPriceInUSDC

    
    # FIXME: Add logic to get amounts desired and amount minimums
    def addLiquidity(self, tokenA, tokenB, amountADesired, amountBDesired, amountAMin, amountBMin):
        function = self.contract.functions.addLiquidity(
            tokenA, tokenB, amountADesired, amountBDesired, amountAMin, amountBMin, userWallet.address, userWallet.getDeadline()
        )
        
        return userWallet.processTransaction(function)


    # FIXME:
    def addLiquidityETH(self, payableAmount, token, amountTokenDesired, amountTokenMin, amountETHMin):
        userWallet.txParams["value"] = int(payableAmount) * pow(10, 18)
        function = self.contract.functions.addLiquidityETH(
            token, amountTokenDesired, amountTokenMin, amountETHMin, userWallet.address, userWallet.getDeadline()
        )
        
        return userWallet.processTransaction(function)


    # FIXME:
    def removeLiquidity(self, lpAddr):
        lpToken = UniswapV2LPtoken(lpAddr)
        token = ERC20(lpAddr)
        tokenA = lpToken.getToken0()
        tokenB = lpToken.getToken1()
        liquidity = token.getBalanceOf(userWallet.address) * 0.999
        lpTotalSupply = lpToken.getTotalSupply()
        userPoolPercentage = liquidity / lpTotalSupply
        lpReserves = lpToken.getReserves()
        amountAMin = int(lpReserves[0] * userPoolPercentage * 0.99)
        amountBMin = int(lpReserves[1] * userPoolPercentage * 0.99)
        userWallet.txParams["value"] = int(liquidity)
        
        return {
            "tokenA" : tokenA,
            "tokenB" : tokenB,
            "liquidity" : liquidity,
            "lpTotalSupply" : lpTotalSupply,
            "userPoolPercentage" : userPoolPercentage,
            "amountAMin" : amountAMin,
            "amountBMin" : amountBMin,
            "value" : userWallet.txParams["value"],
            "deadline" : userWallet.getDeadline()

        }

        '''
        function = self.contract.functions.removeLiquidity(
            tokenA, tokenB, int(liquidity), int(amountAMin), int(amountBMin), userWallet.address, userWallet.getDeadline()
        )
        
        return userWallet.processTransaction(function)
        '''
'''
a = UniswapV2Router(addresses["QuickswapRouter"])
print(a.removeLiquidity(Web3.toChecksumAddress('0x0df9e46c0eaedf41b9d4bbe2cea2af6e8181b033')))
'''