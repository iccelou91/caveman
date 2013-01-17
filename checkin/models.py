from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ClimberProfile(models.Model):
    user = models.ForeignKey(User);
    #real student ID numbers are always 9 digits, but we'll allow one extra
    idnum = models.CharField(max_length=10)
    #only store whether the climber is paid through current term
    feePaid = models.BooleanField(False)
    #only store wheter the climber has signed waiver for current year
    waiverSigned = models.BooleanField(False)
    def __unicode__(self):
        return self.user.username
class CheckOut(models.Model):
    climber = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.climber.username

class CheckIn(models.Model):
    climber = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)
    checkOut = models.ForeignKey(CheckOut, null=True, blank=True)
    def __unicode__(self):
        return self.climber.username
