import json
import os

from decouple import config
from django.conf import settings
from web3 import HTTPProvider, Web3
from web3.exceptions import ContractLogicError

BLOCKCHAIN_URL = config("BLOCKCHAIN_URL")


class BlockchainUserManager:

    PORT = 7545
    PATH = os.path.join(settings.BASE_DIR, "blockchain", "users", "build", "contracts", "Users.json")

    def __init__(self):
        self.web3 = Web3(HTTPProvider(f"{BLOCKCHAIN_URL}:{self.PORT}"))

        self.payer = self.web3.eth.accounts[0]

        with open(self.PATH) as file:
            data = json.load(file)
            self.contract = self.web3.eth.contract(
                self.web3.to_checksum_address(data["networks"]["5777"]["address"]), abi=data["abi"]
            )

    def get_transaction(self, txHash):
        return self.web3.eth.get_transaction(txHash)

    def create_user(self, passport, full_name, birthday):
        try:
            txHash = self.contract.functions.createUser(passport, full_name, birthday).transact({"from": self.payer})
            return txHash
        except ContractLogicError:
            return None

    def get_user(self, passport):
        try:
            return self.contract.functions.getUser(passport).call()
        except ValueError:
            return None


class BlockchainVotingManager:

    PORT = 7546
    PATH = os.path.join(settings.BASE_DIR, "blockchain", "voting", "build", "contracts", "Voting.json")

    def __init__(self):
        self.web3 = Web3(HTTPProvider(f"{BLOCKCHAIN_URL}:{self.PORT}"))

        self.payer = self.web3.eth.accounts[0]

        with open(self.PATH) as file:
            data = json.load(file)
            self.contract = self.web3.eth.contract(
                self.web3.to_checksum_address(data["networks"]["5777"]["address"]), abi=data["abi"]
            )

    def get_transaction(self, txHash):
        return self.web3.eth.get_transaction(txHash)

    def create_ballot(self, title, options, duration):
        try:
            tx_hash = self.contract.functions.createBallot(title, options, duration).transact({"from": self.payer})
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            events = self.contract.events.BallotCreated().process_receipt(tx_receipt)
            address = events[0].args.ballotAddress
            return tx_hash, address
        except ContractLogicError:
            return None, None

    def get_ballot(self, address):
        try:
            return self.contract.functions.getBallot(address).call()
        except ValueError:
            return None

    def has_ended(self, address):
        try:
            return self.contract.functions.hasEnded(address).call()
        except ValueError:
            return None

    def has_vote(self, address, passport):
        try:
            return self.contract.functions.hasVote(address, passport).call()
        except ValueError:
            return None

    def get_vote_counts(self, address):
        try:
            return self.contract.functions.getVoteCounts(address).call()
        except ValueError:
            return None

    def vote(self, ballot_address, passport, option):
        try:
            txHash = self.contract.functions.vote(ballot_address, passport, option).transact({"from": self.payer})
            return txHash
        except (ContractLogicError, ValueError):
            return None
