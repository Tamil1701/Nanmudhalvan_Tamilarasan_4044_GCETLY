from django.db import models
from django.utils import timezone


class Userdetail(models.Model):
    user_id=models.BigAutoField(primary_key=True)
    username=models.CharField(max_length=30)
    email=models.CharField(max_length=30)
    password=models.CharField(max_length=30)

class Question(models.Model):
    question_id=models.BigAutoField(primary_key=True)
    question=models.CharField(max_length=200)
    result_date=models.DateTimeField(default=timezone.now)

class Option(models.Model):
    option_id=models.BigAutoField(primary_key=True)
    option=models.CharField(max_length=100)
    question_id=models.ForeignKey(Question,on_delete=models.CASCADE)

class Poll(models.Model):
    poll_id=models.BigAutoField(primary_key=True)
    user_id=models.ForeignKey(Userdetail,on_delete=models.CASCADE)
    option_id=models.ForeignKey(Option,on_delete=models.CASCADE)
    question_id=models.ForeignKey(Question,on_delete=models.CASCADE)