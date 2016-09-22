from django.db import models
from django.contrib.auth.models import User

class PeriodSetting(models.Model):
    name = models.CharField(max_length=30)
    sortNo = models.IntegerField()
    entryStartDate = models.DateTimeField()
    entryEndDate = models.DateTimeField()
    voteStartDate = models.DateTimeField()
    voteendDate = models.DateTimeField()
    def __str__ (self): return self.name

class AppealPoint(models.Model):
    task = models.TextField()
    process = models.TextField()
    result = models.TextField()
    force = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    insTm = models.DateTimeField(auto_now_add=True)
    updTm = models.DateTimeField(auto_now=True)

class Vote(models.Model):
    appealPoint = models.ForeignKey(AppealPoint, on_delete=models.CASCADE)
    typeCd = models.CharField(max_length=1)    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    insTm = models.DateTimeField(auto_now_add=True)
    updTm = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    appealPoint = models.ForeignKey(AppealPoint, on_delete=models.CASCADE)
    detail = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    insTm = models.DateTimeField(auto_now_add=True)
    updTm = models.DateTimeField(auto_now=True)
    def __str__ (self): return self.detail
