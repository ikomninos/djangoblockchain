from django.contrib.auth.models import User
from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=250)
    data = models.TextField()
    hash = models.CharField(max_length=250)
    nonce = models.IntegerField()
    prev = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
