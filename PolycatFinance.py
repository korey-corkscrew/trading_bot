from wallet import wallet
from web3 import Web3
from web3.middleware import geth_poa_middleware


from ABIs import abiList
from addresses import addresses
from UniswapV2Router import UniswapV2Router
from web3Connect import loadWeb3
from ERC20 import ERC20
from AuguryPoolIDs import AuguryPoolIDs
from UniswapV2LpToken import UniswapV2LPtoken
from AuguryFinance import AuguryFinance

#---------------------------------------------------------
# Load Web3
#---------------------------------------------------------
w3 = loadWeb3()
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

userWallet = wallet()


#---------------------------------------------------------
# CLASS : PolycatMasterChef
#
# FUNCTIONS :
#   __init__()
#   
#---------------------------------------------------------
class PolycatMasterChef:
    def __init__(self):
        self.contract = w3.eth.contract(address=addresses["PolycatMasterChef"], abi=abiList["PolycatMasterChef"])








    def getPendingFish(self, poolID):
        return self.masterChefContract.functions.pendingFish(poolID, userWallet.address).call()

    def getPoolExistence(self, LP_Address):
        return self.masterChefContract.functions.poolExistence(LP_Address).call()

    def getPoolInfo(self, poolID):
        return self.masterChefContract.functions.poolInfo(poolID).call()

    def getPoolLength(self):
        return self.masterChefContract.functions.poolLength().call()

    def getUserInfo(self, poolID):
        return self.masterChefContract.functions.userInfo(poolID, userWallet.address).call()

    def printPoolInfo(self, poolID):
        if(poolID == 1):
            lpToken = LP_Token(self.getPoolInfo(poolID)[0])
            print("Augury Finance: Pool " + str(poolID))
            lpToken.printAllInfo()

        else:
            token = ERC20(self.getPoolInfo(poolID)[0])
            print("Augury Finance: Pool " + str(poolID))
            token.printAllInfo()
            print("Pool Supply: " + str("{:,.4f}".format(token.getBalanceOf(addresses["AuguryFinance"]))))



    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # The following functions are writing to the contract.
    # Contract functions are only called. Additional logic required.

    def deposit(self, poolID, amount, referrer):
        return self.masterChefContract.functions.deposit(poolID, amount, referrer).call()

    def withdraw(self, poolID, amount):
        return self.masterChefContract.functions.withdraw(poolID, amount).call()



#---------------------------------------------------------
# CLASS : PolycatVaultChef
#
# FUNCTIONS :
#   __init__()
#   
#---------------------------------------------------------
class PolycatVaultChef:
    def __init__(self):
        self.contract = w3.eth.contract(address=addresses["PolycatVaultChef"], abi=abiList["PolycatVaultChef"])

    def getPoolInfo(self, poolID):
        info =  self.contract.functions.poolInfo(poolID).call()
        return {
            "tokenAddr" : info[0],
            "stratAddr" : info[1]
        }

    def getPoolLength(self):
        return {
            "poolLength" : self.contract.functions.poolLength().call()
        }

    def getStakedWantTokens(self, poolID):
        return {
            "stakedWantTokens" : self.contract.functions.stakedWantTokens(poolID, userWallet.address).call()
        }
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # The following functions are writing to the contract.
    # Contract functions are only called. Additional logic required.
   
    '''
    def deposit(self, senderAddress, poolID, wantAmount):
        return self.contract.functions.deposit(senderAddress, poolID, wantAmount).call()
    '''

    def deposit(self, poolID, wantAmount):
        function = self.contract.functions.deposit(poolID, wantAmount)
        return userWallet.processTransaction(function)

    '''
    def withdraw(self, senderAddress, poolID, wantAmount):
        return self.vaultChefContract.functions.withdraw(senderAddress, poolID, wantAmount).call()
    '''

    def withdraw(self, poolID, wantAmount):
        function = self.contract.functions.withdraw(poolID, wantAmount)
        return userWallet.processTransaction(function)

    def withdrawAll(self, poolID):
        function = self.contract.functions.withdrawAll(poolID)
        return userWallet.processTransaction(function)

class Polycat:
    def __init__(self):
        self.vault = PolycatVaultChef()
        self.master = PolycatMasterChef()

    