from addresses import addresses
from AuguryPoolIDs import AuguryPoolIDs
from AuguryFinance import AuguryFinance
from Router import Router
import time
import sqlite3
from ERC20 import ERC20
from UniswapV2LpToken import UniswapV2LPtoken
import web3.exceptions



con = sqlite3.connect('AuguryV4.db')
cur = con.cursor()

# Create table
try:
    cur.execute('''CREATE TABLE data
              (date text, tokenAddress text, tokenSymbol text, tokenPrice_Quickswap real, userPoolSupply real, userPoolSupplyValue real, userPendingOMEN real, OMENPrice real, userPendingOMENValue real)''')
except sqlite3.OperationalError:
    pass

con.close()


#---------------------------------------------------------
# Instantiate Exchanges & Protocols
#---------------------------------------------------------
Quickswap = Router(addresses["QuickswapRouter"])
Sushiswap = Router(addresses["SushiswapRouter"])
Augury = AuguryFinance()

def commit():
    try:
        return con.commit()
    except sqlite3.OperationalError:
        print("DB Locked")
        time.sleep(1)
        commit()

def lpTokenCheck(tokenAddr):
    lpToken = UniswapV2LPtoken(tokenAddr)

    if(lpToken.getReserves() == False):
        return {
            "lpToken" : False,
            "symbol" : lpToken.getName()
        }
    else:
        return {
            "lpToken" : True,
            "symbol" : lpToken.getName()
        }



while True:
    # Start with first pool
    poolID = 0

    # Loop through each pool
    while(poolID < Augury.getPoolLength()["poolLength"]):
        tokenAddr = Augury.getPoolInfo(poolID)["tokenAddr"]
        token = lpTokenCheck(tokenAddr)
        OMENPrice = Quickswap.getPriceInUSDC(addresses["OMEN"])
        userStakedTokens = Augury.getUserInfo(poolID)["amount"] * pow(10, -18)
        userPendingOMEN = Augury.getPendingOmen(poolID)["pendingOmen"] * pow(10, -18)
        tokenSymbol = token["symbol"]
        
        if(token["lpToken"]):
            tokenPrice = None
            userStakedPrice = None

        else:
            tokenPrice = Quickswap.getPriceInUSDC(tokenAddr)
            if(tokenPrice == None):
                userStakedPrice == None
            else:
                userStakedPrice = tokenPrice * userStakedTokens


        con = sqlite3.connect('AuguryV4.db')
        cur = con.cursor()
        cur.execute(
            "insert into data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
            (str(time.time()), 
            tokenAddr,
            tokenSymbol,
            tokenPrice, 
            userStakedTokens,
            userStakedPrice,
            userPendingOMEN,
            OMENPrice,
            userPendingOMEN * OMENPrice
            )
        )
        commit()
        con.close()
        poolID = poolID + 1
    time.sleep(120)
