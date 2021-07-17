from web3 import Web3
from web3.middleware import geth_poa_middleware
from ABIs import abiList
from addresses import addresses
from web3Connect import loadWeb3
from ERC20 import ERC20
from AuguryPoolIDs import AuguryPoolIDs
from UniswapV2LpToken import UniswapV2LPtoken
from wallet import wallet
from Router import Router
import time
import sqlite3
from pandas import read_sql_query, read_sql_table
import pandas as pd



#---------------------------------------------------------
# Load Web3
#---------------------------------------------------------
w3 = loadWeb3()
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


#---------------------------------------------------------
# Get user wallet information
#---------------------------------------------------------
userWallet = wallet()


#---------------------------------------------------------
# Quickswap router for swaps & adding/removing pool liquidity 
#---------------------------------------------------------
Quickswap = Router(addresses["QuickswapRouter"])


#---------------------------------------------------------
# CLASS : AuguryFinance
#
# FUNCTIONS :
#   __init__()
#   getPendingOmen(poolID)
#   getPoolExistence(LP_Address)
#   getPoolInfo(poolID)
#   getPoolLength()
#
#---------------------------------------------------------
class AuguryFinance:

    #-----------------------------------------------------
    # FUNCTION : 
    #   
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   N/A
    #-----------------------------------------------------
    def __init__(self):
        self.contract = w3.eth.contract(address=addresses["AuguryFinance"], abi=abiList["AuguryFinance"])
        self.userAddress = userWallet.account.address


    #-----------------------------------------------------
    # FUNCTION : 
    #   
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   N/A
    #-----------------------------------------------------
    def getPendingOmen(self, poolID):
        return {
            "pendingOmen" : self.contract.functions.pendingOmen(poolID, self.userAddress).call()
        }


    #-----------------------------------------------------
    # FUNCTION : 
    #   
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   N/A
    #-----------------------------------------------------
    def getPoolExistence(self, LP_Address):
        return self.contract.functions.poolExistence(LP_Address).call()


    #-----------------------------------------------------
    # FUNCTION : 
    #   
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   N/A
    #-----------------------------------------------------
    def getPoolInfo(self, poolID):
        info =  self.contract.functions.poolInfo(poolID).call()
        return {
            "tokenAddr" : info[0],
            "allocPoint" : info[1],
            "lastRewardBlock" : info[2],
            "accOmenPerShare" : info[3],
            "depositFeePercent" : info[4]
        }


    #-----------------------------------------------------
    # FUNCTION : 
    #   
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   N/A
    #-----------------------------------------------------
    # Returns number of active pools 
    def getPoolLength(self):
        return {
            "poolLength" : self.contract.functions.poolLength().call()
        }


    #-----------------------------------------------------
    # FUNCTION : 
    #   
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   N/A
    #-----------------------------------------------------
    def getUserInfo(self, poolID):
        info = self.contract.functions.userInfo(poolID, self.userAddress).call()
        return {
            "amount" : info[0],
            "rewardDebt" : info[1]
        }


    #-----------------------------------------------------
    # FUNCTION : 
    #   
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   N/A
    #-----------------------------------------------------
    def getAllUserInfo(self):
        poolLength = self.getPoolLength()["poolLength"]

        poolID = 0

        info = {}

        while(poolID < poolLength):
            userInfo = self.getUserInfo(poolID)
            userPending = self.getPendingOmen(poolID)
            token = ERC20(self.getPoolInfo(poolID)["tokenAddr"])

            if(poolID == 1 or poolID == 17 or poolID == 18):
                info[poolID] = {
                    "amount" : userInfo["amount"],
                    "rewardDebt" : userInfo["rewardDebt"],
                    "pendingOmen" : userPending["pendingOmen"],
                    "poolSupply" : token.getBalanceOf(addresses["AuguryFinance"]),
                    "lpToken" : Quickswap.getLpTokenData(self.getPoolInfo(poolID)["tokenAddr"])
                }

            else:
                info[poolID] = {
                    "amount" : userInfo["amount"],
                    "rewardDebt" : userInfo["rewardDebt"],
                    "pendingOmen" : userPending["pendingOmen"],
                    "poolSupply" : token.getBalanceOf(addresses["AuguryFinance"]),
                    "token" : token.getAllInfo(),
                }
            poolID = poolID + 1

        return info


    #-----------------------------------------------------
    # FUNCTION : harvest
    #   Harvests pool rewards
    #
    # INPUTS :
    #   poolID - Pool to harvest rewards from
    #
    # OUTPUT :
    #   Transaction receipt
    #-----------------------------------------------------
    def harvest(self, poolID):
        function = self.contract.functions.deposit(poolID, 0, userWallet.address)
        return userWallet.processTransaction(function)


    #-----------------------------------------------------
    # FUNCTION : deposit
    #   Deposits tokens into pool
    #
    # INPUTS :
    #   poolID - Pool to deposit into
    #   amount - Amount of tokens to deposit into pool
    #
    # OUTPUT :
    #   Transaction receipt
    #-----------------------------------------------------
    def deposit(self, poolID, amount):
        function = self.contract.functions.deposit(poolID, amount, addresses["Referrer"])
        return userWallet.processTransaction(function)


    #-----------------------------------------------------
    # FUNCTION : withdraw
    #   Withdraws staked tokens from pool.
    #
    # INPUTS :
    #   poolID - Pool to deposit into
    #   amount - Amount of tokens to deposit into pool
    #
    # OUTPUT :
    #   Transaction receipt
    #-----------------------------------------------------
    def withdraw(self, poolID, amount):
        function = self.contract.functions.withdraw(poolID, amount)
        return userWallet.processTransaction(function)


    #-----------------------------------------------------
    # FUNCTION : harvestAllPendingOMENSwapForUSDC
    #   Harvests all rewards from each pool then swaps all
    #   rewards for USDC.
    #
    # INPUTS :
    #   N/A
    #
    # OUTPUT :
    #   Transaction details
    #-----------------------------------------------------
    def harvestAllPendingOMENSwapForUSDC(self):

        # Start with first pool
        poolID = 0
        totalOMEN = 0

        # Loop through each pool
        while(poolID < self.getPoolLength()["poolLength"]):

            # Get pending OMEN for pool
            pendingOMEN = self.getPendingOmen(poolID)["pendingOmen"]

            # Pool has pending OMEN
            if(pendingOMEN > 0):

                # Harvest rewards from pool
                transactionHarv = self.harvest(poolID)

                # Transaction unsuccessful - attempt to harvest again
                while(transactionHarv["status"] == 0):
                    transactionHarv = self.harvest(poolID)
                
                # Print transaction details
                print("Harvest - Pool " + str(poolID) + ":")
                print(transactionHarv)

                # Add pool rewards to total rewards
                totalOMEN += pendingOMEN

            # Move to next pool
            poolID += 1

        # Swap all withdrawn tokens from pool to USDC
        transactionSwap = Quickswap.swapExact(totalOMEN, addresses["OMEN"], addresses["USDC"])

        # Transaction unsuccessful - attempt to swap again
        while(transactionSwap["status"] == 0):
            transactionSwap = Quickswap.swapExact(totalOMEN, addresses["OMEN"], addresses["USDC"])

        # Calculate USDC received estimate
        USDCReceived = Quickswap.getPriceInUSDC(addresses["OMEN"]) * totalOMEN

        # Return transaction details
        return {
            "totalOMENHarvested" : totalOMEN * pow(10, -18),
            "USDCReceived" : USDCReceived * pow(10, -18)
        }


    #-----------------------------------------------------
    # FUNCTION : poolSellStop
    #   Harvests rewards, withdraws all staked tokens, and
    #   swaps withdrawn tokens to USDC when token price
    #   falls below sell stop price.
    #
    # INPUTS :
    #   poolID - Pool to set sell stop for
    #   stopPrice - Sell stop price in USD
    #
    # OUTPUT :
    #   Details from all three transactions
    #-----------------------------------------------------
    '''
    def poolSellStop(self, poolID, stopPrice):
        token = ERC20(self.getPoolInfo(poolID)["tokenAddr"])

        # Get token price
        tokenPrice = Quickswap.getPriceInUSDC(token.tokenAddress)

        # Token price falls below sell stop price
        if(Quickswap.getPriceInUSDC(token.tokenAddress) <= stopPrice):

            # Get user amount staked in pool
            amount = self.getUserInfo(poolID)["amount"]

            # Harvest rewards from pool
            transactionHarv = self.harvest(poolID)

            # Transaction unsuccessful - attempt to harvest again
            while(transactionHarv["status"] == 0):
                transactionHarv = self.harvest(poolID)
            
            # Print transaction details
            print("Harvest:")
            print(transactionHarv)

            # Withdraw all user tokens from pool
            transactionWith = self.withdraw(poolID, amount)

            # Transaction unsuccessful - attempt to withdraw again
            while(transactionWith["status"] == 0):
                transactionWith = self.withdraw(poolID, amount)
            
            # Print transaction details
            print("\nWithdraw:")
            print(transactionWith)

            # Swap all withdrawn tokens from pool to USDC
            transactionSwap = Quickswap.swapExact(amount, token.tokenAddress, addresses["USDC"])

            # Transaction unsuccessful - attempt to swap again
            while(transactionSwap["status"] == 0):
                transactionSwap = Quickswap.swapExact(amount, token.tokenAddress, addresses["USDC"])
            
            # Print transaction details
            print("\nSwap:")
            print(transactionSwap)

            # Return all details
            return {
                "timeStamp" : time.time(),
                "fromToken" : token.getSymbol(),
                "fromAmount" : amount,
                "fromTokenPrice" : tokenPrice,
                "stopPrice" : stopPrice,
                "toToken" : "USDC",
                "toAmount" : amount * tokenPrice
            }

        # Token price above sell stop price
        else:
            return False
    '''

    def poolSellStop(self, sellPrice):
        '''
        con = sqlite3.connect('AuguryV4.db')
        df = pd.read_sql_query("SELECT * FROM data", con)
        print(df["date"].iloc[-1])
        '''

        '''
        # Token price falls below sell stop price
        cursor = cur.execute('SELECT date, tokenPrice_Quickswap from data WHERE tokenAddress=(?) ORDER by date DESC',(tokenAddr))
        currPrice = cursor.fetchone()[1]
        con.close()
        print(currPrice)
        data=pd.read_sql_query("SELECT * FROM Reviews",con)
        '''

        currPrice = Quickswap.getPriceInUSDC(addresses["OMEN"])
        if(currPrice <= sellPrice):

            # Get user amount staked in pool
            amount = self.getUserInfo(AuguryPoolIDs["OMEN"])["amount"]

            # Harvest rewards from pool
            transactionHarv = self.harvest(AuguryPoolIDs["OMEN"])

            # Transaction unsuccessful - attempt to harvest again
            while(transactionHarv["status"] == 0):
                transactionHarv = self.harvest(AuguryPoolIDs["OMEN"])
            
            # Print transaction details
            print("Harvest:")
            print(transactionHarv)

            # Withdraw all user tokens from pool
            transactionWith = self.withdraw(AuguryPoolIDs["OMEN"], amount)

            # Transaction unsuccessful - attempt to withdraw again
            while(transactionWith["status"] == 0):
                transactionWith = self.withdraw(AuguryPoolIDs["OMEN"], amount)
            
            # Print transaction details
            print("\nWithdraw:")
            print(transactionWith)

            # Swap all withdrawn tokens from pool to USDC
            transactionSwap = Quickswap.swapExact(amount, addresses["OMEN"], addresses["USDC"])

            # Transaction unsuccessful - attempt to swap again
            while(transactionSwap["status"] == 0):
                transactionSwap = Quickswap.swapExact(amount, addresses["OMEN"], addresses["USDC"])
            
            # Print transaction details
            print("\nSwap:")
            print(transactionSwap)
            print()

            # Return all details
            return {
                "timeStamp" : time.time(),
                "fromToken" : "OMEN",
                "fromAmount" : amount,
                "fromTokenPrice" : currPrice,
                "stopPrice" : sellPrice,
                "toToken" : "USDC",
                "toAmount" : amount * currPrice
            }

        # Token price above sell stop price
        else:
            return False


    #-----------------------------------------------------
    # FUNCTION : poolTrailingSellStop
    #   Harvests rewards, withdraws all staked tokens, and
    #   swaps withdrawn tokens to USDC when token price
    #   falls below sell stop price.
    #
    # INPUTS :
    #   poolID - Pool to set sell stop for
    #   stopPrice - Sell stop price in USD
    #
    # OUTPUT :
    #   Details from all three transactions
    #-----------------------------------------------------
    '''
    def poolTrailingSellStop(self, poolID, percentLoss):
        token = ERC20(self.getPoolInfo(poolID)["tokenAddr"])

        # Get token price
        tokenPrice = Quickswap.getPriceInUSDC(token.tokenAddress)

        # Token price falls below sell stop price
        if(Quickswap.getPriceInUSDC(token.tokenAddress) <= stopPrice):

            # Get user amount staked in pool
            amount = self.getUserInfo(poolID)["amount"]

            # Harvest rewards from pool
            transactionHarv = self.harvest(poolID)

            # Transaction unsuccessful - attempt to harvest again
            while(transactionHarv["status"] == 0):
                transactionHarv = self.harvest(poolID)
            
            # Print transaction details
            print("Harvest:")
            print(transactionHarv)

            # Withdraw all user tokens from pool
            transactionWith = self.withdraw(poolID, amount)

            # Transaction unsuccessful - attempt to withdraw again
            while(transactionWith["status"] == 0):
                transactionWith = self.withdraw(poolID, amount)
            
            # Print transaction details
            print("\nWithdraw:")
            print(transactionWith)

            # Swap all withdrawn tokens from pool to USDC
            transactionSwap = Quickswap.swapExact(amount, token.tokenAddress, addresses["USDC"])

            # Transaction unsuccessful - attempt to swap again
            while(transactionSwap["status"] == 0):
                transactionSwap = Quickswap.swapExact(amount, token.tokenAddress, addresses["USDC"])
            
            # Print transaction details
            print("\nSwap:")
            print(transactionSwap)

            # Return all details
            return {
                "timeStamp" : time.time(),
                "fromToken" : token.getSymbol(),
                "fromAmount" : amount,
                "fromTokenPrice" : tokenPrice,
                "stopPrice" : stopPrice,
                "toToken" : "USDC",
                "toAmount" : amount * tokenPrice
            }

        # Token price above sell stop price
        else:
            return False
    '''