import web3
from addresses import addresses
from AuguryPoolIDs import AuguryPoolIDs
from AuguryFinance import AuguryFinance
from PolycatFinance import PolycatMasterChef, PolycatVaultChef
from wallet import wallet
from Router import Router
from AAVE import AAVE_Finance
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3Connect import loadWeb3
import time


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

w3 = loadWeb3()
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

#print(Augury.harvestAllPendingOMENSwapForUSDC())


print(Augury.poolSellStop(0.2060, addresses["OMEN"]))
'''
monitor = True
while(monitor):
    transaction = Augury.poolSellStop(0.2060, addresses["OMEN"])
    if(transaction == False):
        time.sleep(15)
    else:
        monitor = False
        print(transaction)
'''
