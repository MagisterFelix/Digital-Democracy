from django.db import models


class BallotManager(models.Manager):

    def create(self, ballot_id, tx_hash, **extra_fields):
        ballot = self.model(
            id=ballot_id,
            tx_hash=tx_hash,
            **extra_fields
        )
        ballot.save()

        return ballot


class Ballot(models.Model):

    id = models.CharField(
        max_length=128,
        primary_key=True,
        unique=True,
        error_messages={
            "unique": "A ballot with that id already exists.",
        })
    tx_hash = models.CharField(max_length=128)

    objects = BallotManager()

    def __str__(self):
        return self.id

    class Meta:
        db_table = "ballot"
