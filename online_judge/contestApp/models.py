from django.db import models
from judge.models import Problem
from django.contrib.auth.models import User

# Create your models here.
class Contest(models.Model):
    name = models.CharField(max_length=63)
    description = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.name

class ContestProblem(Problem):
    points = models.IntegerField(default=0)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)

class Scorecard(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest,on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
