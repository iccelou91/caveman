# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from forms import CheckInOutForm
from django import forms

from models import CheckIn, CheckOut

def checkInClimber(user):
    print "checking in", user
    lastCheckIn = CheckIn.objects.filter(climber=user, checkOut=None)
    if lastCheckIn:
        raise ValueError

    checkIn = CheckIn(climber=user)
    checkIn.save()


def checkOutClimber(user):
    print "checking out", user
    lastCheckIn = CheckIn.objects.filter(climber=user, checkOut=None)
    if not lastCheckIn:
        raise ValueError

    lastCheckIn = lastCheckIn[0]
    checkOut = CheckOut(climber=user)
    checkOut.save()
    lastCheckIn.checkOut = checkOut
    lastCheckIn.save()


def checkIn(request):
    if request.method == 'POST':
        form = CheckInOutForm(request.POST)
        form.fields['isCheckIn'].widget = forms.HiddenInput()
        if form.is_valid():
            user = form.cleaned_data['user']
            if form.cleaned_data["isCheckIn"]:
                result = checkInClimber(user)
            if not form.cleaned_data["isCheckIn"]:
                result = checkOutClimber(user)
            return HttpResponseRedirect('/')
    else:
        form = CheckInOutForm()
        form.fields['isCheckIn'].widget = forms.HiddenInput()

    return render(request, 'form.html', {'form': form, })


def test(request):
    return render(request, 'form.html', {})
