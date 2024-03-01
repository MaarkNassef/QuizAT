from django.db import models
from django.utils import timezone
from groups.models import Group
from accounts.models import CustomUser

class Quiz(models.Model):
    title = models.CharField(max_length=255, default='--')
    start_time = models.DateTimeField(default=timezone.now)
    duration = models.DurationField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=None)

    def __str__(self) -> str:
        return self.title
    
    def get_duration_in_minutes(self) -> int:
        return self.duration.seconds // 60

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self) -> str:
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.text
    
class Grade(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    right_answers = models.IntegerField()
    total_questions = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.student.full_name}'s grade"