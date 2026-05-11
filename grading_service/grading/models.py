from django.db import models
class Grade(models.Model):
    submission_id = models.IntegerField(unique=True)
    marks = models.PositiveIntegerField()
    feedback = models.TextField()
    graded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Grade for Submission {self.submission_id}"
