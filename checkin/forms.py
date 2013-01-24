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
     
class ClimberRegistrationForm(forms.Form):
    username = forms.CharField(max_length = 50)
    first_name = forms.CharField(label="First Name",max_length = 20)
    last_name = forms.CharField(label="Last Name", max_length = 20)
    email = forms.EmailField()
    student_id = forms.CharField(label="Student ID Number")
    def clean(self):
        cleaned_data = super(ClimberRegistrationForm, self).clean()
        usernameData = cleaned_data.get('username')
        if(User.objects.filter(username = usernameData).count() >= 1):
            raise forms.ValidationError("A climber with that username already exists.")
        
        return cleaned_data
    
