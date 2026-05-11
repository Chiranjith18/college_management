from django.db import models
from django.conf import settings
class Submission(models.Model):
    student_id = models.IntegerField()
    assignment_id = models.IntegerField()
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Student {self.student_id} - Assignment {self.assignment_id}"
