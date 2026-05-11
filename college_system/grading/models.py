from django.db import models
from submissions.models import Submission

class Grade(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='grade')
    marks = models.PositiveIntegerField()
    feedback = models.TextField()
    graded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Grade for {self.submission}"
