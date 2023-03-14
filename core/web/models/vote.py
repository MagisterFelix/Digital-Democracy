from django.db import models


class VoteManager(models.Manager):

    def create(self, address=None, **extra_fields):
        vote = self.model(
            address=address,
            **extra_fields
        )
        vote.save()

        return vote


class Vote(models.Model):

    address = models.CharField(
        max_length=128,
        primary_key=True,
        unique=True,
        error_messages={
            "unique": "A vote with that address already exists.",
        })

    objects = VoteManager()

    def __str__(self):
        return self.address

    class Meta:
        db_table = "vote"
