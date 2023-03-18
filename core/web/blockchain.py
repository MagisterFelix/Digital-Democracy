import json
import os
from datetime import datetime

from decouple import config
from django.conf import settings
from web3 import HTTPProvider, Web3
from web3.exceptions import ContractLogicError

BLOCKCHAIN_URL = config("BLOCKCHAIN_URL")


class BlockchainUserManager:

    PORT = 7545
    PATH = os.path.join(settings.BASE_DIR, "blockchain", "users", "build", "contracts", "Users.json")

    def __init__(self):
        self._web3 = Web3(HTTPProvider(f"{BLOCKCHAIN_URL}:{self.PORT}"))

        self._payer = self._web3.eth.accounts[0]

        with open(self.PATH) as file:
            data = json.load(file)
            self._contract = self._web3.eth.contract(
                self._web3.to_checksum_address(data["networks"]["5777"]["address"]), abi=data["abi"]
            )

    def create_user(self, passport, full_name, birthday):
        try:
            tx_hash = self._contract.functions.createUser(
                passport, full_name, birthday).transact({"from": self._payer})
            return self._web3.to_hex(tx_hash)
        except ContractLogicError:
            return None

    def get_user(self, passport):
        try:
            return self._contract.functions.getUser(passport).call()
        except ValueError:
            return None


class BlockchainVotingManager:

    PORT = 7546
    PATH = os.path.join(settings.BASE_DIR, "blockchain", "voting", "build", "contracts", "Voting.json")

    def __init__(self):
        self._web3 = Web3(HTTPProvider(f"{BLOCKCHAIN_URL}:{self.PORT}"))

        self._payer = self._web3.eth.accounts[0]

        with open(self.PATH) as file:
            data = json.load(file)
            self._contract = self._web3.eth.contract(
                self._web3.to_checksum_address(data["networks"]["5777"]["address"]), abi=data["abi"]
            )

    def get_transaction(self, tx_hash):
        transaction = self._web3.eth.get_transaction(tx_hash)
        transaction = {
            "hash": self._web3.to_hex(transaction.hash),
            "block_number": transaction.blockNumber,
            "block_hash": self._web3.to_hex(transaction.blockHash),
            "block_timestamp": datetime.fromtimestamp(self._web3.eth.get_block(transaction.blockNumber).timestamp),
            "from": transaction["from"],
            "to": transaction["to"],
            "gas_price": transaction.gasPrice,
            "gas": transaction.gas,
            "nonce": transaction.nonce,
            "input": transaction.input,
        }
        return transaction

    def create_ballot(self, title, options, end_date):
        try:
            tx_hash = self._contract.functions.createBallot(title, options, end_date).transact({"from": self._payer})
            tx_receipt = self._web3.eth.wait_for_transaction_receipt(tx_hash)
            events = self._contract.events.BallotCreated().process_receipt(tx_receipt)
            ballot_id = events[0].args.id
            return self._web3.to_hex(tx_hash), self._web3.to_hex(ballot_id)
        except ContractLogicError:
            return None, None

    def get_ballot(self, ballot_id):
        try:
            return self._contract.functions.getBallot(ballot_id).call()
        except ValueError:
            return None

    def get_vote(self, ballot_id, passport):
        try:
            return self._contract.functions.getVote(ballot_id, passport).call()
        except ValueError:
            return None

    def vote(self, ballot_id, passport, option):
        try:
            tx_hash = self._contract.functions.vote(ballot_id, passport, option).transact({"from": self._payer})
            return self._web3.to_hex(tx_hash)
        except (ContractLogicError, ValueError):
            return None
