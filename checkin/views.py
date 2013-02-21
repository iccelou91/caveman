# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from forms import GetClimberForm, ClimberRegistrationForm, WaiverForm
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
    return redirect('/')

def close_cave(request):
    unclosed = CaveOpening.objects.filter(close_time__isnull=True)
    for opening in unclosed:
        if(opening.opener==request.user):
            opening.close()
    return redirect('/')
    
def get_climber(request):
    if request.method == 'POST':
        form = GetClimberForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            climber = ClimberProfile.objects.get(user=user)
            #TODO this url
            return redirect('/dashboard/'+climber.id_num)
    else:
        form = GetClimberForm()

    return render(request, 'homepage_form.html', {'form': form, })
    
def check_in_climber(request, student_id):
    climber = ClimberProfile.objects.get(id_num=student_id)
    opening = CaveOpening.objects.get(close_time__isnull=True)
    #TODO expiration of waivers and fees
    if(climber.waiver_last_signed):
        if(climber.fee_last_paid):
            opening.climbers.add(climber)
            opening.save()
        else:
            raise ValueError("Climber has not paid fee!")
    else:
        raise ValueError("Climber has not signed waiver!")
    return redirect('/')
    
def sign_waiver(request, student_id):
    climber = ClimberProfile.objects.get(id_num=student_id)
    #TODO render a form with waiver and update sign date if user submits it
    if request.method == 'POST':
        form = WaiverForm(request.POST)
        if form.is_valid():
            climber = ClimberProfile.objects.get(id_num=student_id)
            climber.waiver_last_signed = datetime.now()
            climber.save()
            return redirect('/')
    else:
        form = WaiverForm()
    return render(request, 'waiver.html', {'form': form, })
    
def pay_fee(request, student_id):
    climber = ClimberProfile.objects.get(id_num=student_id)
    request = PaymentApprovalRequest(requester=climber)
    request.save()
    return redirect('/')
    
def get_climber_dashboard(request, student_id):
    climber = ClimberProfile.objects.get(id_num=student_id)
    is_staff = climber.user.is_staff
    is_open = False
    if(is_staff):
        if len(CaveOpening.objects.filter(close_time__isnull=True)) != 0:
            is_open = True
    return render(request, 'dashboard.html', {'student_id': student_id, 'climber':climber, 'is_staff':is_staff, 'is_open':is_open})
    
def sign_up(request):
    #TODO registration via form
    if request.method == 'POST':
        form = ClimberRegistrationForm(request.POST)                                                   #make a user form filled with information from request.post
        if form.is_valid():                                                             #clean the data and store them in a new_user instance if the form is valid
            new_user = User(is_staff = False, is_superuser = False, is_active = False)
            new_user.username = form.cleaned_data['username']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.email = form.cleaned_data['email']
            new_user.set_unusable_password() #regular climbers can't log in
            new_user.save()
            new_climber = ClimberProfile(user=new_user, id_num=form.cleaned_data['student_id'])
            new_climber.first_name = form.cleaned_data['first_name']
            new_climber.last_name = form.cleaned_data['last_name']
            new_climber.save()
            return redirect('/dashboard/'+new_climber.id_num)
    else:
        form = ClimberRegistrationForm()
    return render(request, 'registration_form.html',{
            'form': form
    })
