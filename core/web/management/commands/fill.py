import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from core.web.blockchain import BlockchainUserManager
from core.web.models import User


class Command(BaseCommand):
    help = "Fill blockchain and database with test user data"

    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, "core", "web", "management", "db_gen_peoples.json")
        with open(path) as file:
            json_obj = json.load(file)

        b_user_manager = BlockchainUserManager()

        for idx, people in enumerate(json_obj):
            passport, name, birthday, email, password = people.values()
            tx = b_user_manager.create_user(passport=passport, full_name=name, birthday=birthday)

            if idx == 0:
                User.objects.create_superuser(passport=passport, email=email, password=password)
            elif tx:
                User.objects.create_user(passport=passport, email=email, password=password)

        self.stdout.write(self.style.SUCCESS("Successfully filled"))
