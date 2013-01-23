# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from forms import GetClimberForm
from django import forms
from django.contrib.auth.decorators import login_required
from models import *

@login_required
def open_cave(request):
    unclosed = CaveOpening.objects.filter(close_time__isnull=True)
    for opening in unclosed:
        opening.close()
    new_opening = CaveOpening(opener=request.user)
    new_opening.save()

def get_climber(request):
    if request.method == 'POST':
        form = GetClimberForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            climber = Climber.objects.get(user=user)
            #TODO this url
            redirect('/dashboard/'+climber.id_num)
    else:
        form = GetClimberForm()

    return render(request, 'form.html', {'form': form, })
    
def get_climber_dashboard(request, student_id):
    climber = ClimberProfile.objects.get(id_num=student_id)
    #TODO render a template with that climber's dashboard
    
def check_in_climber(request, student_id):
    climber = ClimberProfile.objects.get(id_num=student_id)
    opening = CaveOpening.objects.get(close_time__isnull=True)
    #TODO expiration of waivers and fees
    if(climber.waiver_last_signed):
        if(climber.fee_last_paid):
            opening.climbers.add(climber)
            opening.save()
        else:
            raise ValueError
    else:
        raise ValueError
    redirect('/')
    
def sign_waiver(request, student_id):
    climber = ClimberProfile.objects.get(id_num=student_id)
    #TODO render a form with waiver and update sign date if user submits it
    if request.method == 'POST':
        form = WaiverForm(request.POST)
        if form.is_valid():
            climber = ClimberProfile.objects.get(user=request.user)
            climber.waiver_last_signed = datetime.now()
            climber.save()
            redirect('/')
    else:
        form = WaiverForm()
    return render(request, 'waiver.html', {'form': form, })
    
def pay_fee(request, student_id):
    climber = ClimberProfile.objects.get(id_num=student_id)
    request = PaymentApprovalRequest(requester=climber)
    request.save()
    
def sign_up(request):
    pass
    #TODO registration via form
