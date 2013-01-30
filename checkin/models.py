from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class ClimberProfile(models.Model):
    user = models.ForeignKey(User, blank=True, null=True);
    #real student ID numbers are always 9 digits, but we'll allow one extra
    id_num = models.CharField(max_length=10, primary_key=True)
    fee_last_paid = models.DateTimeField(blank=True, null=True)
    waiver_last_signed = models.DateTimeField(blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)
    def __unicode__(self):
        return self.get_full_name()
        
class CaveOpening(models.Model):
    opener = models.ForeignKey(User)
    open_time = models.DateTimeField(auto_now_add=True)
    close_time = models.DateTimeField(blank=True, null=True)
    climbers = models.ManyToManyField(ClimberProfile)
    def close(self):
        self.close_time = datetime.now()
        self.save()
    def __unicode__(self):
        return '%s to %s(%s)' % (self.open_time, self.close_time, self.opener.username)

class PaymentApprovalRequest(models.Model):
    requester = models.ForeignKey(ClimberProfile)
    date = models.DateTimeField(auto_now_add=True)
    def approve(self):
        self.requester.fee_last_paid = self.date
        self.requester.save()
        self.delete()
    def reject(self):
        self.delete()
        
