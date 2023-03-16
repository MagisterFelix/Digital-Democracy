from django.db import models


class BallotManager(models.Manager):

    def create(self, address=None, **extra_fields):
        ballot = self.model(
            address=address,
            **extra_fields
        )
        ballot.save()

        return ballot


class Ballot(models.Model):

    address = models.CharField(
        max_length=128,
        primary_key=True,
        unique=True,
        error_messages={
            "unique": "A ballot with that address already exists.",
        })

    objects = BallotManager()

    def __str__(self):
        return self.address

    class Meta:
        db_table = "ballot"
