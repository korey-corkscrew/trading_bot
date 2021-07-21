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
from UniswapV2Router import UniswapV2Router
import time
import datetime


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


#print(Augury.poolSellStop(0.117))
total = 0

def arb(fromToken, toToken, fromAmount):
    amountOut1 = UniswapV2Router(addresses['QuickswapRouter']).getAmountsOut(fromAmount, [fromToken, toToken])[-1]
    amountOut2 = UniswapV2Router(addresses['SushiswapRouter']).getAmountsOut(amountOut1, [toToken, fromToken])[-1]
    
    print(datetime.datetime.now())
    print(fromAmount * pow(10, -6))
    print(amountOut2 * pow(10, -6))

    diff = amountOut2 - fromAmount
    print(diff * pow(10, -6))
    print()

    '''
    if(diff > 0):
        print(datetime.datetime.now())
        print(diff)
        print()
        return diff
    else:
        return 0
    '''




while True:
    arb(addresses['USDC'], addresses['WETH'], 1000000000)
    #print(diff)
    #print()
    '''
    if(diff > 0):
        total = total + diff
        print("Total: " + str(total))
    '''
    time.sleep(5)



'''
monitor = True
while(monitor):
    transaction = Augury.poolSellStop(0.117)
    if(transaction == False):
        time.sleep(15)
    else:
        monitor = False
        print(transaction)
'''

