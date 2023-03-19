from django.db import models

from .user import User


class Log(models.Model):

    class Action(models.IntegerChoices):
        INTERACTION = 0, "Interaction"
        LOGIN_ATTEMPT = 1, "Login attempt"
        BALLOT_CREATION_ATTEMPT = 2, "Ballot creation attempt"
        VOTING_ATTEMPT = 3, "Voting attempt"

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.IntegerField(choices=Action.choices, default=Action.INTERACTION)
    ip = models.CharField(max_length=128)
    location = models.CharField(max_length=128)

    def __str__(self):
        return self.created_at.isoformat()

    class Meta:
        db_table = "log"
