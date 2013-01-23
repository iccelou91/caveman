from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from models import *

class GetClimberForm(forms.Form):
    username = forms.CharField()

    def clean(self):
        cleaned_data = super(GetClimberForm, self).clean()
        #user, created = User.objects.get_or_create(username=cleaned_data['username'])
        #if created:
            #print "this is a new user"
            #user.is_active = False
        try:
            user = User.objects.get(username=cleaned_data['username'])
        except ObjectDoesNotExist:
            raise forms.ValidationError("%s does not exist" % cleaned_data['username'])
        cleaned_data["user"] = user

        return cleaned_data
        
class WaiverForm(forms.Form):
    accepted = forms.BooleanField(False)
    signature = forms.CharField()
    
    def clean(self):
        cleaned_data = super(WaiverForm, self).clean()
        if not accepted:
            raise forms.ValidationError("You must accept the terms before climbing")
        return cleaned_data
