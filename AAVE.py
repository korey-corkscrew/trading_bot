from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.types import TxReceipt
from ABIs import abiList
from addresses import addresses
from web3Connect import loadWeb3
import time
from ERC20 import ERC20
from wallet import wallet
import json


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
#   Use to get market prices on Quickswap
#
# FUNCTIONS :
#   __init__()
#   getFactory()
#   getAmountIn(amountOut, reserveIn, reserveOut)
#   getAmountOut(amountIn, reserveIn, reserveOut)
#   getAmountsIn(amoutnOut, *path)
#   getAmountsOut(amountIn, *path)
#---------------------------------------------------------
class AAVE_WETH_GATEWAY:

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
    def __init__(self):
        self.w3 = loadWeb3()
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.contract = w3.eth.contract(address=addresses["AAVE_WETH_GATEWAY"], abi=abiList["AAVE_WETH_GATEWAY"])


    #-----------------------------------------------------
    # FUNCTION : 
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #-----------------------------------------------------
    def borrowETH(self, lendingPool, amount, interestRateMode, referralCode):
        function = self.contract.functions.borrowETH(lendingPool, amount, interestRateMode, referralCode)
        return userWallet.processTransaction(function)


    #-----------------------------------------------------
    # FUNCTION : 
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #-----------------------------------------------------
    def depositETH(self, payableAmount):
        payableAmount = payableAmount * pow(10, 18)
        userWallet.txParams["value"] = int(payableAmount)
        function = self.contract.functions.depositETH(Web3.toChecksumAddress('8dff5e27ea6b7ac08ebfdf9eb090f32ee9a30fcf'), userWallet.address, 0)
        return userWallet.processTransaction(function)

    
    #-----------------------------------------------------
    # FUNCTION : 
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #-----------------------------------------------------
    def repayETH(self, payableAmount, lendingPool, amount, interestRateMode, onBehalfOf):
        function = self.contract.functions.repayETH(payableAmount, lendingPool, amount, interestRateMode, onBehalfOf)
        return userWallet.processTransaction(function)


    #-----------------------------------------------------
    # FUNCTION : 
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #-----------------------------------------------------
    def withdrawETH(self, lendingPool, amount, to):
        function = self.contract.functions.withdrawETH(lendingPool, amount, to)
        return userWallet.processTransaction(function)


#---------------------------------------------------------
# CLASS : UniswapV2Router
#   Use to get market prices on Quickswap
#
# FUNCTIONS :
#   __init__()
#   getFactory()
#   getAmountIn(amountOut, reserveIn, reserveOut)
#   getAmountOut(amountIn, reserveIn, reserveOut)
#   getAmountsIn(amoutnOut, *path)
#   getAmountsOut(amountIn, *path)
#---------------------------------------------------------
class AAVE_Router:

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
    def __init__(self):
        self.w3 = loadWeb3()
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.contract = w3.eth.contract(address=addresses["AAVE_Router"], abi=abiList["AAVE_Router"])


    #-----------------------------------------------------
    # FUNCTION : 
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #-----------------------------------------------------
    def getReserveData(self, asset):
        return self.contract.functions.getReserveData(asset).call()


    #-----------------------------------------------------
    # FUNCTION : 
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #-----------------------------------------------------
    def getReserveNormalizedIncome(self, asset):
        return self.contract.functions.getReserveNormalizedIncome(asset).call()


    #-----------------------------------------------------
    # FUNCTION : 
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #-----------------------------------------------------
    def getReserveNormalizedVariableDebt(self, asset):
        return self.contract.functions.getReserveNormalizedVariableDebt(asset).call()


    #-----------------------------------------------------
    # FUNCTION : 
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #-----------------------------------------------------
    def getReservesList(self):
        return self.contract.functions.getReservesList().call()


    #-----------------------------------------------------
    # FUNCTION : 
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #-----------------------------------------------------
    def getUserAccountData(self):
        data = self.contract.functions.getUserAccountData(userWallet.address).call()
        return {
            "totalCollateralETH" : data[0],
            "totalDebtETH" : data[1],
            "availableBorrowsETH" : data[2],
            "currentLiquidationThreshold" : data[3],
            "ltv" : data[4],
            "healthFactor" : data[5]
        }


    #-----------------------------------------------------
    # FUNCTION : 
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #-----------------------------------------------------
    def borrow(self, asset, amount, interestRateMode, referralCode, onBehalfOf):
        function = self.contract.functions.borrow(asset, amount, interestRateMode, referralCode, onBehalfOf)
        return userWallet.processTransaction(function)


    #-----------------------------------------------------
    # FUNCTION : 
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #-----------------------------------------------------
    def deposit(self, asset, amount):
        token = ERC20(asset)
        _amount = amount * pow(10, token.getDecimals())
        function = self.contract.functions.deposit(asset, int(_amount), userWallet.address, 0)
        return userWallet.processTransaction(function)


    #-----------------------------------------------------
    # FUNCTION : 
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #-----------------------------------------------------
    def finalizeTransfer(self, asset, _from, to, amount, balanceFromBefore, balanceToBefore):
        function = self.contract.functions.finalizeTransfer(asset, _from, to, amount, balanceFromBefore, balanceToBefore)
        return userWallet.processTransaction(function)


    #-----------------------------------------------------
    # FUNCTION : 
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #-----------------------------------------------------
    def flashLoan(self, receiverAddress, assets, amounts, modes, onBehalfOf, params, referralCode):
        function = self.contract.functions.flashLoan(receiverAddress, assets, amounts, modes, onBehalfOf, params, referralCode)
        return userWallet.processTransaction(function)


    #-----------------------------------------------------
    # FUNCTION : 
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #-----------------------------------------------------
    def repay(self, asset, amount, rateMode, onBehalfOf):
        function = self.contract.functions.repay(asset, amount, rateMode, onBehalfOf)
        return userWallet.processTransaction(function)


    #-----------------------------------------------------
    # FUNCTION : 
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #-----------------------------------------------------
    def withdraw(self, asset, amount, to):
        function = self.contract.functions.withdraw(asset, amount, to)
        return userWallet.processTransaction(function)

class AAVE_Rewards:
    def __init__(self):
        self.w3 = loadWeb3()
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.contract = w3.eth.contract(address=addresses["AAVE_Rewards"], abi=abiList["AAVE_Rewards"])

    def getRewardsBalance(self, *assets):
        return self.contract.functions.getRewardsBalance(assets, userWallet.address).call()

    def getUserAssetData(self, asset):
        return self.contract.functions.getUserAssetData(userWallet.address, asset).call()

    def getUserUnclaimedRewards(self):
        return self.contract.functions.getUserUnclaimedRewards(userWallet.address).call()


class AAVE_Finance:
    def __init__(self):
        self.WETH_Gateway = AAVE_WETH_GATEWAY()
        self.router = AAVE_Router()
        self.rewards = AAVE_Rewards()

    def deposit(self, token, amount):
        if(token == addresses["MATIC"]):
            return self.WETH_Gateway.depositETH(amount)

        else:
            return self.router.deposit(token, amount)

    # Rewards
    def getRewardsBalance(self, asset):
        assets = [asset]
        return self.rewards.getRewardsBalance(assets)

    def getUserUnclaimedRewards(self):
        return self.rewards.getUserUnclaimedRewards()

    def getUserAssetData(self, asset):
        return self.rewards.getUserAssetData(asset)
    
    def getReservesList(self):
        return self.router.getReservesList()

    def getReserveData(self, asset):
        return self.router.getReserveData(asset)