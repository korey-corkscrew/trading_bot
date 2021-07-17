from web3 import Web3
from web3.middleware import geth_poa_middleware
import requests
import json
from termcolor import colored
import sqlite3
import time
import os


from ABIs import abiList
from addresses import addresses
from UniswapV2Router import UniswapV2Router
from web3Connect import loadWeb3
from ERC20 import ERC20
from AuguryPoolIDs import AuguryPoolIDs
from UniswapV2LpToken import UniswapV2LPtoken
from AuguryFinance import AuguryFinance
from PolycatFinance import PolycatMasterChef, PolycatVaultChef
from wallet import wallet
from Router import Router
from AAVE import AAVE_Finance

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
# Instantiate Exchanges & Protocols
#---------------------------------------------------------
Quickswap = Router(addresses["QuickswapRouter"])
Sushiswap = Router(addresses["SushiswapRouter"])
Augury = AuguryFinance()
AAVE = AAVE_Finance()


#---------------------------------------------------------
# Quickswap Examples
#---------------------------------------------------------

# Get Quickswap LP token data
#------------------------------

#print(Quickswap.getLpTokenData(addresses["OMEN_USDC"]))



# Swap exact token for MATIC on Quickswap
#------------------------------

#print(Quickswap.swapExact(0.5, addresses["USDC"], addresses["MATIC"]))



# Swap token for exact MATIC on Quickswap
#------------------------------

#print(Quickswap.swapForExact(0.5, addresses["USDC"], addresses["MATIC"]))



# Swap MATIC for exact token on Quickswap
#------------------------------

#print(Quickswap.swapForExact(1, addresses["MATIC"], addresses["USDC"]))



# Swap exact MATIC for token on Quickswap
#------------------------------

#print(Quickswap.swapExact(0.5, addresses["MATIC"], addresses["USDC"]))



# Swap exact token for token on Quickswap
#------------------------------

#print(Quickswap.swapExact(0.5, addresses["USDC"], addresses["FISH"]))



# Swap token for exact token on Quickswap
#------------------------------

#print(Quickswap.swapForExact(5, addresses["USDC"], addresses["OMEN"]))




#---------------------------------------------------------
# Sushiswap Examples - Same examples as Quickswap 
#---------------------------------------------------------

# Get token price in USDC
#------------------------------

#print(Sushiswap.getPriceInUSDC(addresses["MATIC"]))



# Swap exact tokens for tokens
#------------------------------

#print(Sushiswap.swapExact(0.5, addresses["USDC"], addresses["FISH"]))




#---------------------------------------------------------
# Augury Finance Examples
#---------------------------------------------------------

# Get data for a single Augury pool
#------------------------------

#print(Augury.getPoolInfo(AuguryPoolIDs["OMEN"]))



# Get user pending OMEN for a single Augury pool
#------------------------------

#print(Augury.getPendingOmen(AuguryPoolIDs["OMEN"]))



# Get user data for a single Augury pool
'''
print(Augury.getUserInfo(AuguryPoolIDs["OMEN"]))
'''

# Get user data for all Augury pools
'''
print(Augury.getAllUserInfo())
'''

# Harvest rewards from pool

#print(Augury.harvest(AuguryPoolIDs["OMEN"]))


# Withdraw staked tokens
'''
print(Augury.withdraw(AuguryPoolIDs["OMEN"], 10))
'''

# Stake tokens in pool
'''
print(Augury.deposit(AuguryPoolIDs["OMEN"], 5))
'''


#---------------------------------------------------------
# AAVE Examples - DOES NOT WORK. FUNCTIONS NEED TO BE COMPLETED.
#---------------------------------------------------------

# Deposit token into pool
'''
print(AAVE.deposit(addresses["MATIC"], 0.5))
'''


'''
print(AAVE.getUserUnclaimedRewards())
'''
'''
print(AAVE.getReservesList())
'''

#print(userWallet.txParams)