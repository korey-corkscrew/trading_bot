from requests.models import Response
from web3 import Web3
import web3
from web3.middleware import geth_poa_middleware
import os
import time
from web3Connect import loadWeb3
from addresses import addresses
import requests


#---------------------------------------------------------
# Load Web3
#---------------------------------------------------------
w3 = loadWeb3()
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


class wallet:

    def __init__(self):
        self.dev = os.getenv("PRIVATE_KEY")
        self.account = w3.eth.account.from_key(self.dev)
        self.address = self.account.address
        self.txParams = {
            "from" : self.address,
            "gas" : 600000,
            "chainId" : 137,
            "gasPrice" : 0,
            "nonce" : w3.eth.getTransactionCount(self.address)
        }

    def getDeadline(self):
        return int(time.time()) + (10 * 60)

    def updateTxParameters(self):
        r = requests.get('https://gasstation-mainnet.matic.network/')
        gas = r.json()
        gasFast = int(gas['fast'] * pow(10, 9))
        gasStandard = int(gas['standard'] * pow(10, 9))

        self.txParams["gasPrice"] = gasStandard
        self.txParams["nonce"] = w3.eth.getTransactionCount(self.address)
        
        return self.txParams


    def processTransaction(self, function):
        try:
            transaction = self._processTransaction(function)
            return {
                "transactionHash" : Web3.toHex(transaction.transactionHash),
                "status" : transaction.status
            }

        except web3.exceptions.TimeExhausted:
            return {
                "status" : 0,
                "error" : "TimeExhausted"
            }
        
        except ValueError:
            return {
                "status" : 0,
                "error" : "ValueError"
            }

        '''
        finally:
            return {
                "status" : 0,
                "error" : "Unknown"
            }
        '''

    def _processTransaction(self, function):
        self.updateTxParameters()
        transaction = function.buildTransaction(self.txParams)
        signed_txn = w3.eth.account.sign_transaction(transaction, str(self.dev))

        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        tx_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
        count = 0
        if tx_receipt is None and (count<30):
            time.sleep(10)
            tx_receipt = w3.eth.getTransactionReceipt(txn_hash)
            
        return tx_receipt