import datetime
import hashlib
import json
import os
import random
import time

from django.conf import settings
from django.core.management.base import BaseCommand

from core.web import bm_user, bm_voting
from core.web.models import Ballot, User


class Command(BaseCommand):
    help = "Fill blockchain and database with test data"

    def handle(self, *args, **options):
        self.create_test_users()
        self.create_test_ballots()
        self.create_test_votes()

        self.stdout.write(self.style.SUCCESS("Successfully filled"))

    @staticmethod
    def create_test_users():
        path = os.path.join(settings.BASE_DIR, "core", "web", "management", "db_gen_peoples.json")
        with open(path) as file:
            people_data = json.load(file)

        admin_passport, _, _, admin_email, admin_password = people_data[0].values()
        User.objects.create_superuser(passport=admin_passport, email=admin_email, password=admin_password)

        for people in people_data[1:]:
            passport, name, birthday, email, password = people.values()
            passport_hash = hashlib.sha256(passport.encode()).hexdigest()

            if bm_user.create_user(passport=passport_hash, full_name=name, birthday=birthday):
                User.objects.create_user(passport=passport, email=email, password=password)

    @staticmethod
    def create_test_ballots():
        path = os.path.join(settings.BASE_DIR, "core", "web", "management", "db_gen_ballots.json")
        with open(path) as file:
            ballot_data = json.load(file)

        for data in ballot_data:
            title, options, duration = data.values()
            end_date = int(time.mktime((datetime.date.today() + datetime.timedelta(seconds=duration)).timetuple()))

            tx_hash, ballot_id = bm_voting.create_ballot(title=title, options=options, end_date=end_date)

            if tx_hash and ballot_id:
                Ballot.objects.create(ballot_id=ballot_id, tx_hash=tx_hash)

    @staticmethod
    def create_test_votes():
        ballots = Ballot.objects.all()
        users = User.objects.filter(is_superuser=False)

        for user in users:
            for ballot in ballots:
                if random.random() > 0.5:
                    options = bm_voting.get_ballot(ballot_id=ballot.id)[1]
                    option = random.randint(1, len(options))

                    bm_voting.vote(ballot_id=ballot.id, passport=user.passport, option=option)
