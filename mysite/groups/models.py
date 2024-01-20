from django.db import models
from accounts.models import CustomUser

class Group(models.Model):
    name = models.CharField(max_length=255)
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='group_admin')
    members = models.ManyToManyField(CustomUser, related_name='group_members')

    def __str__(self):
        return self.name
