from ERC20 import ERC20
import requests
import json
from addresses import addresses
import time
import datetime
from wallet import wallet

userWallet = wallet()
count = 0
total = 0
amountIn = 1000000000 # 1000 USDC
fromToken = '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174' # USDC
toToken = '0x7ceb23fd6bc0add59e62ac25578270cff1b9f619' # WETH
startingTime = datetime.datetime.now()



def swap():
    r = requests.get('https://api.1inch.exchange/v3.0/137/swap?fromTokenAddress=' + fromToken + '&toTokenAddress=' + toToken + '&amount='+ str(amountIn) + '&fromAddress=' + userWallet.address + '&slippage=1').json()
    print(userWallet.processTransaction1Inch(r))
    amount = r['toTokenAmount']
    r = requests.get('https://api.1inch.exchange/v3.0/137/swap?fromTokenAddress=' + toToken + '&toTokenAddress=' + fromToken + '&amount='+ str(ERC20(addresses['WETH']).getBalanceOf(userWallet.address)) + '&fromAddress=' + userWallet.address + '&slippage=1').json()
    print(userWallet.processTransaction1Inch(r))


def swap1(trans1):
    print(userWallet.processTransaction1Inch(trans1))

def swap2():
    try:
        print(userWallet.processTransaction1Inch(requests.get('https://api.1inch.exchange/v3.0/137/swap?fromTokenAddress=' + toToken + '&toTokenAddress=' + fromToken + '&amount='+ str(ERC20(addresses['WETH']).getBalanceOf(userWallet.address)) + '&fromAddress=' + userWallet.address + '&slippage=1').json()))
    except:
        print("Swap 2 Error")
        swap2()


'''
# Successful trade flag
trade = False

# Continue until successful trade
while not trade:
    urlData = None
    urlData1 = None
    WETHAmount = ERC20(addresses['WETH']).getBalanceOf(userWallet.address)
    trans1Error = False
    trans2Error = False
    toAmount = 0
    secondSwap = False
    urlData2 = None
    firstSwap = False

    # First trade
    url = 'https://api.1inch.exchange/v3.0/137/swap?fromTokenAddress=' + fromToken + '&toTokenAddress=' + toToken + '&amount='+ str(amountIn) + '&fromAddress=' + userWallet.address + '&slippage=1'

    # Get to token amount
    try:
        urlData = requests.get(url).json()
        toAmount = urlData['toTokenAmount']
    
    # Exception handling - Print error message
    except KeyError:
        trans1Error = True
        print(datetime.datetime.now())
        print("Error: API Call For 1st Quote Failed")
        print(urlData)
        print()

    # 1st API successful
    if not trans1Error:
        try:
            # Second Trade
            urlData1 = requests.get('https://api.1inch.exchange/v3.0/137/quote?fromTokenAddress=' + toToken + '&toTokenAddress=' + fromToken + '&amount=' + str(toAmount)).json()
            returnAmount = urlData1['toTokenAmount']

        # Exception handling - Print error message
        except KeyError:
            trans2Error = True
            print(datetime.datetime.now())
            print("Error: API Call For 2nd Quote Failed")
            print(urlData1)
            print()

    # Both API calls successful
    if not trans1Error and not trans2Error:

        # Find difference between starting/ending amount
        amountDiff = (int(returnAmount) - amountIn) * pow(10, -6)
        
        # Print time and amount difference
        print(datetime.datetime.now())
        print(amountDiff)
        print()
        
        # Amount difference is profitable
        if(amountDiff > 0.10):
            print(datetime.datetime.now())
            print(amountDiff)
            print()

            # Perform 1st swap
            tx = userWallet.processTransaction1Inch(urlData)
            print("1st Swap:")
            print(tx)
            print()

            # 
            if(tx['status'] != 1):
                tx = userWallet.processTransaction1Inch(urlData)
                print("Error: 1st Swap")
                print(tx)
                print()

            else:
                firstSwap = True
            
            if firstSwap:
                while not secondSwap:
                    try:
                        urlData2 = requests.get('https://api.1inch.exchange/v3.0/137/swap?fromTokenAddress=' + toToken + '&toTokenAddress=' + fromToken + '&amount='+ str(ERC20(addresses['WETH']).getBalanceOf(userWallet.address)) + '&fromAddress=' + userWallet.address + '&slippage=1').json()
                        toAmount2 = urlData['toTokenAmount']
                        secondSwap = True
            
                    # Exception handling - Print error message
                    except KeyError:
                        print(datetime.datetime.now())
                        print("Error: API Call For 2nd Swap Failed")
                        print(urlData2)
                        print()

                tx = userWallet.processTransaction1Inch(urlData2)
                print("2nd Swap:")
                print(tx)
                print()
                if(tx['status'] != 1):
                    tx = userWallet.processTransaction1Inch(urlData2)
                    print("Error: 2nd Swap")
                    print(tx)
                    print()
                
    time.sleep(1)
'''



while True:

    # First trade
    r = requests.get('https://api.1inch.exchange/v3.0/137/quote?fromTokenAddress=' + fromToken + '&toTokenAddress=' + toToken + '&amount=' + str(amountIn))
    data = r.json()

    # Get to token amount
    try:
        toAmount = data['toTokenAmount']
        r1 = requests.get('https://api.1inch.exchange/v3.0/137/quote?fromTokenAddress=' + toToken + '&toTokenAddress=' + fromToken + '&amount=' + str(toAmount))
        data1 = r1.json()

    # Exception handling - Print error message
    except KeyError:
        print(datetime.datetime.now())
        print(data)
        print()

    # Find difference between the two trades (> 0 = Profitable trades)
    try:
        diff = (int(data1['toTokenAmount']) - amountIn) * pow(10, -6)
        # Profit over $0.00
        if(diff > 0):
            total = total + diff
            count = count + 1

            print(datetime.datetime.now())
            print(diff)
            print("\nSince: " + str(startingTime))
            print("Total: " + str(total) + " from " + str(count) + " trades")
            print()

    # Exception handling - Get error message
    except KeyError:
        print(datetime.datetime.now())
        print(data1)
        print()

    
    time.sleep(5)

