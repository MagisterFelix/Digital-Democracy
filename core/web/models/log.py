from django.db import models

from .user import User


class Log(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip = models.CharField(max_length=128)
    location = models.CharField(max_length=128)

    def __str__(self):
        return self.recorded_at.isoformat()

    class Meta:
        db_table = "log"
