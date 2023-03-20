import os
import random

import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Fill train data"

    def handle(self, *args, **options):
        self.generate_sample()

        self.stdout.write(self.style.SUCCESS("Successfully generated"))

    @staticmethod
    def generate_sample():
        path = os.path.join(settings.BASE_DIR, "core", "web", "machine_learning", "data", "user_behavior.csv")

        data = []
        user_dict = {}

        for _ in range(1000):
            ip = f"{random.randint(0, 9)}.{random.randint(0, 9)}.{random.randint(0, 9)}.{random.randint(0, 9)}"
            user_id = chr(ord("a") + random.randint(0, 9))

            for _ in range(10):
                if user_id not in user_dict:
                    user_dict[user_id] = ip
                    action = 1
                    is_fraud = 0
                else:
                    action = random.randint(0, 3)
                    if action == 1 and random.random() > 0.5:
                        action = 0

                    if action == 1:
                        if user_dict[user_id] == ip:
                            is_fraud = 0
                        else:
                            if random.random() > 0.5:
                                is_fraud = 0
                                for _ in range(random.randint(1, 3)):
                                    data.append([action, ip, user_id, is_fraud])
                            else:
                                is_fraud = 1
                                for _ in range(random.randint(4, 6)):
                                    data.append([action, ip, user_id, 1])
                    else:
                        is_fraud = int(user_dict[user_id] != ip)

                data.append([action, ip, user_id, is_fraud])

        df = pd.DataFrame(data, columns=["action", "ip", "user_id", "is_fraud"])
        df.to_csv(path, index=False)
