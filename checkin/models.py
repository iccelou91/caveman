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
    def check_in_climber(self, climber):
        if(self.validate_waiver(climber)):
            if(self.validate_fee(climber)):
                self.climbers.add(climber)
                self.save()
            else:
                raise ValueError("Climber has not paid fee!")
        else:
            raise ValueError("Climber has not signed waiver!")
    def validate_waiver(self, climber):
        if(climber.waiver_last_signed):
            return True
        else:
            return False
    def validate_fee(self, climber):
        if(climber.fee_last_paid):
            return True
        else:
            return False
    def close(self):
        self.close_time = datetime.now()
        self.save()
    def __unicode__(self):
        return '%s to %s(%s)' % (self.open_time, self.close_time, self.opener.username)

class FreeCaveOpening(CaveOpening):
    def check_in_climber(self, climber):
        if(self.validate_waiver):
            opening.climbers.add(climber)
        else:
            raise ValueError("Climber has not signed waiver!")
class PaymentApprovalRequest(models.Model):
    requester = models.ForeignKey(ClimberProfile)
    date = models.DateTimeField(auto_now_add=True)
    def approve(self):
        self.requester.fee_last_paid = self.date
        self.requester.save()
        self.delete()
    def reject(self):
        self.delete()
        
