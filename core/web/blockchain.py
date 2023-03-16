import json
import web3
from web3.exceptions import ContractLogicError

BLOCKCHAIN_URL = "http://127.0.0.1:7545"
USERS_ABI_PATH = "../../blockchain/build/contracts/Users.json"
PAYER_ADDRESS = ...
w3 = web3.Web3(web3.HTTPProvider(BLOCKCHAIN_URL))
USERS_CONTRACT_ADDRESS = w3.to_checksum_address(...)
with open(USERS_ABI_PATH) as json_file:
    json_obj = json.load(json_file)
    ABI = json_obj['abi']

users_contract = w3.eth.contract(USERS_CONTRACT_ADDRESS, abi=ABI)


def get_blockchain_user(passport_hash: str):
    try:
        user_id, user_data = users_contract.functions.getUser(passport_hash).call()
        return user_id, user_data
    except ValueError as e:
        print(e.args[0]["message"])


def create_blockchain_user(passport_hash: str, user_data: str):
    try:
        users_contract.functions.createUser(passport_hash, user_data).transact(
            {"from": PAYER_ADDRESS})
        return True
    except ContractLogicError as e:
        print(e)
