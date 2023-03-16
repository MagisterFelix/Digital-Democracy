import json
import web3
from web3.exceptions import ContractLogicError

BLOCKCHAIN_URL = "http://127.0.0.1"
USERS_BLOCKCHAIN_PORT = 7545
VOTES_BLOCKCHAIN_PORT = 7546

USERS_PAYER_ADDRESS = ...
VOTES_PAYER_ADDRESS = ...

USERS_CONTRACT_ADDRESS = ...
VOTES_CONTRACT_ADDRESS = ...

USERS_ABI_PATH = "../../blockchain/build/contracts/Users.json"
VOTES_ABI_PATH = "../../blockchain/voting/build/contracts/Voting.json"

users_w3 = web3.Web3(web3.HTTPProvider(f"{BLOCKCHAIN_URL}:{USERS_BLOCKCHAIN_PORT}"))
votes_w3 = web3.Web3(web3.HTTPProvider(f"{BLOCKCHAIN_URL}:{VOTES_BLOCKCHAIN_PORT}"))

users_contract_address = users_w3.to_checksum_address(USERS_CONTRACT_ADDRESS)
votes_contract_address = votes_w3.to_checksum_address(VOTES_CONTRACT_ADDRESS)

with open(USERS_ABI_PATH) as json_file:
    _json_obj = json.load(json_file)
    USERS_ABI = _json_obj['abi']

users_contract = users_w3.eth.contract(users_contract_address, abi=USERS_ABI)

with open(VOTES_ABI_PATH) as json_file:
    _json_obj = json.load(json_file)
    VOTES_ABI = _json_obj['abi']

votes_contract = votes_w3.eth.contract(votes_contract_address, abi=VOTES_ABI)


def get_blockchain_user(passport_hash: str):
    try:
        user_id, user_data = users_contract.functions.getUser(passport_hash).call()
        return user_id, user_data
    except ValueError as e:
        print(e.args[0]["message"])


def create_blockchain_user(passport_hash: str, user_data: str):
    try:
        users_contract.functions.createUser(passport_hash, user_data).transact({"from": USERS_PAYER_ADDRESS})
        return True
    except ContractLogicError as e:
        print(e)


def create_bill(title: str, options: list[str], duration: int):
    try:
        votes_contract.functions.createBill(title, options, duration).transact({"from": VOTES_PAYER_ADDRESS})
        return True
    except Exception as e:
        print(e)


def get_bill_options(bill_id: int):
    try:
        options = votes_contract.functions.getBillOptions(bill_id).call()
        return options
    except ValueError as e:
        print(e.args[0]["message"])


def vote(bill_id: int, option_index: int, passport_hash: str):
    if not get_blockchain_user(passport_hash):
        return None
    try:
        votes_contract.functions.vote(bill_id, option_index, passport_hash).transact({"from": VOTES_PAYER_ADDRESS})
    except ContractLogicError as e:
        print(e)
    except ValueError as e:
        print(e)
