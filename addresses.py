from web3 import Web3
from web3.middleware import geth_poa_middleware


#---------------------------------------------------------
# Addresses
#---------------------------------------------------------
addresses = {
    #"Wallet" : Web3.toChecksumAddress('0x3ce06FAFA62c028BD0197Ad12591264e44126D53'),
    "OMEN_USDC" : Web3.toChecksumAddress('0x50409de292f5f821888702e9538bf15fa273dfe6'),
    "WBTC_WETH" : Web3.toChecksumAddress('0xdc9232e2df177d7a12fdff6ecbab114e2231198d'),
    "QuickswapRouter" : Web3.toChecksumAddress('0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff'), #Quickswap
    "QuickswapFactory" : Web3.toChecksumAddress('0x5757371414417b8C6CAad45bAeF941aBc7d3Ab32'),
    "AuguryFinance" : Web3.toChecksumAddress('0x6ad70613d14c34aa69E1604af91c39e0591a132e'),
    "PolycatMasterChef" : Web3.toChecksumAddress('0x8CFD1B9B7478E7B0422916B72d1DB6A9D513D734'),
    "PolycatVaultChef" : Web3.toChecksumAddress('0xf2E8fC408d77e8fC012797654D76ed399BFcE174'),
    "USDC" : Web3.toChecksumAddress('0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'),
    "SushiswapRouter" : Web3.toChecksumAddress('0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506'),
    "SushiswapFactory" : '0x6e71edae12b1b97f4d1f60370fef10105fa2faae0126114a169c64845d6126c9',
    "MATIC" : Web3.toChecksumAddress('0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'),
    "DAI" : Web3.toChecksumAddress('0x8f3cf7ad23cd3cadbd9735aff958023239c6a063'),
    "FISH" : Web3.toChecksumAddress('0x3a3df212b7aa91aa0402b9035b098891d276572b'),
    "OMEN" : Web3.toChecksumAddress('0x76e63a3e7ba1e2e61d3da86a87479f983de89a7e'),
    "Referrer" : Web3.toChecksumAddress('0x0000000000000000000000000000000000000000'),
    "QUICK" : Web3.toChecksumAddress('0x831753DD7087CaC61aB5644b308642cc1c33Dc13'),
    "WMATIC-WETH" : Web3.toChecksumAddress('0xc4e595acDD7d12feC385E5dA5D43160e8A0bAC0E'),
    "AAVE_WETH_GATEWAY" : Web3.toChecksumAddress('0xbEadf48d62aCC944a06EEaE0A9054A90E5A7dc97'),
    "AAVE_Router" : Web3.toChecksumAddress('0x8dFf5E27EA6b7AC08EbFdf9eB090F32ee9a30fcf'),
    "AAVE_Rewards" : Web3.toChecksumAddress('0x357D51124f59836DeD84c8a1730D72B749d8BC23')
}