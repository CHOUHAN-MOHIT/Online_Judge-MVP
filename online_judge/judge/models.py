from sqlite3 import Timestamp
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Problem(models.Model):
    Difficulty_choices = (
    ('difficult' , 'difficult'),
    ('medium' , 'medium'),
    ('easy' , 'easy'),
    )
    problem_name = models.CharField(max_length=63)
    problem_desc = models.CharField(max_length=255)
    problem_difficulty = models.CharField(max_length=10, choices=Difficulty_choices)

    def __str__(self):
        return self.problem_name

class Test(models.Model):
    problem = models.ForeignKey(Problem , on_delete=models.CASCADE)
    test_input = models.CharField(max_length=255)
    test_output = models.CharField(max_length=255)



class Solution(models.Model):
    Language_choices = (
        ('c++' , 'cpp'),
    )
    Verdict_choices = (
        ('PS' , 'Processing'),
        ('WA' , 'Wrong Answer'),
        ('AC' , 'All Correct'),
    )
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem , on_delete=models.CASCADE)
    language = models.CharField(max_length=10 , choices=Language_choices)
    code_file = models.CharField(max_length=255)
    verdict = models.CharField(max_length=5 , choices=Verdict_choices)
    timestamp = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " submitted " + self.problem.problem_name