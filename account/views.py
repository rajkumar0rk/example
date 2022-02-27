import re
from base64 import urlsafe_b64decode
from email.message import EmailMessage

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import RegistrationForm
from .models import Account


# Create your views here.
def login(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"Login Success")
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid Login Credentials')
            return redirect('login')
    return render(request,'account/login.html')

def register(request):
    if request.method == 'POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name'] 
            last_name=form.cleaned_data['last_name']
            phone_number=form.cleaned_data['phone_number'] 
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            username=email.split("@")[0]
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
            user.phone_number=phone_number
            user.save()

            #USER ACTIVATION
            current_site=get_current_site(request)
            mail_subject='Please Activate Your Account'
            message=render_to_string('account/account_verification_email.html',{
                'user': user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email= email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            return redirect('/account/login/?command=verification&email='+email)
    else:
        form=RegistrationForm()
        context={'form':form}
    return render(request,'account/register.html',context)
@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request,"Logout Successfully")
    return redirect('login')
    
def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(ValueError,TypeError,OverflowError,Account.DoesNotExist):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Your Email is Activated Successfull')
        return redirect('login')
    else:
        messages.error(request,'Invalid Activation Link')
        return redirect('register')
    
def dashboard(request):
    return render(request,'account/dashboard.html')

def forgetpassword(request):
    if request.method == 'POST':
        email=request.POST['email']
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)
         #USER ACTIVATION
            current_site=get_current_site(request)
            mail_subject='Reset Your Password'
            message=render_to_string('account/reset_password_email.html',{
                'user': user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email= email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Password Reset Email Has Been Sent To Your Mail Address')
            return redirect('login')
        else:
            messages.error(request,'Account Does Not Exist')
            return redirect('forgetpassword')
    return render(request,'account/forgetpassword.html')

def reset_password_validation(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(ValueError,TypeError,OverflowError,Account.DoesNotExist):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Please Reset your Password')
        return redirect('reset_password')
    else:
        messages.error(request,'Reset Link Has Been Expired!')
        return redirect('login')

def reset_password(request):
    if request.method == 'POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password == confirm_password:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password Reset Successfull')
            return redirect('login')
        else:
            messages.error(request,'Password Do Not Match!')
            return redirect('reset_password')
    else:
        return render(request,'account/reset_password.html')
