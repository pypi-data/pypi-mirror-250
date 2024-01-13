from spectral_cli.abis.abis import load_abis
import os
CONFIG_PATH = os.path.expanduser("~/.spectral/config.ini")
ALCHEMY_URL = "https://arb-mainnet.g.alchemy.com/v2/"
ABIS = load_abis()
MODELER_CONTRACT = "0xbbd73A046a9022F272BD2f3dC2B43a4449b066b3"
PRIMARY_IPFS_LINK = "http://silver-absent-kite-292.mypinata.cloud/ipfs/"
SUBSCRIPTION_LIB_URL = "https://subscription-library.spectral.finance"
VALIDATOR_WALLET_ADDRESS = "0xc001C50946AF123B8dD85171B05F43000feCfA22"
CHAIN_ID = 42161
GAS = 4000000
GAS_PRICE_GWEI = '0.12'
TX_EXPLORER_URL = "https://arbiscan.io/tx"
CREDIT_SCORING_CHALLENGE_SETTINGS = {
    "contract_address": "0xFDC1BE05aD924e6Fc4Ab2c6443279fF7C0AB5544",
    "training_dataset_ipfs_cid": "QmTqZdaVrHmh9kQFhEjeobk1p4FkhDB2uwZMUHsh6fgMcB",
    "inferences_to_submit": 10000,
    "proofs_to_submit": 10,
    "submission_features_start_column": 3
}

PLUMBER_URL = 'https://plumber.spectral.finance'

os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
