from django.db import models

# Create your models here.
class Test(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)

class EventItem(models.Model):
    Id = models.CharField(max_length=200, primary_key=True)
    StartTime = models.DateTimeField(null=True)
    EndTime = models.DateTimeField(null=True)
    Duration = models.TimeField(null=True)
    Creator = models.CharField(max_length=50, null=True)

class Entry(models.Model):    pub_date = models.DateField([...])