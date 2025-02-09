from django.db import models

class Question(models.Model):
    question = models.TextField()
    response = models.TextField(blank=True, null=True)
    is_human = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
