from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title