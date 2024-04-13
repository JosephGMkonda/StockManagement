import email
from os import link
from urllib import request
from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth
from django.urls import reverse
from django.utils.encoding import force_bytes,DjangoUnicodeDecodeError,force_str
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str

# Create your views here.

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email= data['email']

        if not validate_email(email):
            return JsonResponse({"email_error":"Email is invalid"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"email_error":"Email in use please choose another one"}, status=409)
        return JsonResponse({'email_valid':True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({"username_error":"username should only contain alphanumeric characters"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"username_error":"sorry username in use, choose another one"}, status=409)
        return JsonResponse({'username_valid':True})





class RegistrationView(View):
    def get(self, request):
        return render(request,'authentication/register.html')


    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues':request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request,'the password is too short')
                    return render(request,'authentication/register.html',context)

                user =User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                uidb64=urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link=reverse('verification', kwargs={"uidb64":uidb64,"token":token_generator.make_token(user)})
                
                activate_url="http://"+domain+link
                email_body="Hi "+ user.username + " Please use this link to activate your account\n"+activate_url
                email_subject='Activate your account'
                email = EmailMessage(
                    email_subject,
                    email_body,
                'noreply@semycolon.com',
                [email],
                
                )
                email.send(fail_silently=False)
                messages.success(request,"Account successfully created check email to activate it")
                return render(request,'authentication/register.html')
      
        return render(request,'authentication/register.html')

class VerificationView(View):
    def get(self,request,uidb64,token):
        
        try:

            id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=id)

            if not token_generator.check_token(user,token):
                return redirect('login'+'?message='+'user already activated')
            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request,'Account is activated successfully')
            return redirect('login')

        except Exception as ex:
            pass


        return redirect('login')


class LoginView(View):
    def get(self,request):
        return render(request,'authentication/login.html')

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request,"Welcome "+user.username+" you are now logged in")
                    return redirect('dashboard')

                messages.success(request,"Account is not active, please check your emails ")

                return render(request,'authentication/login.html')
            messages.success(request,"Invalid credentils,try again ")

            return render(request,'authentication/login.html')
        messages.success(request,"please fill all fields ")

        return render(request,'authentication/login.html')


class LogoutView(View):
    def post(self,request):
        auth.logout(request)
        messages.success(request,'You have been logged out')
        return redirect('login')


class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, "authentication/reset_password.html")
    def post(self, request):

        email = request.POST['email']
        context = {
            'values': request.POST
        }
        if not validate_email(email):
            messages.error(request, "Please Supply valid email")
            return render(request, "authentication/reset_password.html", context)
        


        domain = get_current_site(request)
        user = User.objects.filter(email=email).first()

        if user.pk is not None:
            uidb64=urlsafe_base64_encode(force_bytes(user.pk))
            link=reverse('resetpassword', kwargs={"uidb64":uidb64,"token":PasswordResetTokenGenerator().make_token(user)})
            reset_url="http://"+domain.domain+link
            email_body="Hi there Please use this link to reset your password for your account\n"+reset_url
            email_subject='Reset Your Password'
            email = EmailMessage(
                    email_subject,
                    email_body,
                'noreply@semycolon.com',
                [email],
                
                )
            email.send(fail_silently=False)
        messages.success(request, 'We have sent you an email to reset your password')
        return render(request, "authentication/reset_password.html")

class CompletePasswordReset(View):
    def get(self, request,uidb64,token):
        context = {
            "uidb64":uidb64,
            "token": token
        }

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.info(request, 'Password link is invalid, please request new one')
                return render(request, "authentication/reset_password.html")

            
            
        except Exception as identifier:
            pass
        return render(request, 'authentication/set_newpassword.html', context)
    
    def post(self, request, uidb64, token):
        context = {
            "uidb64":uidb64,
            "token": token
        }

        password=request.POST['password']
        password2=request.POST['password2']

        if password != password2:
            messages.error(request,'Passwords do not match')
            return render(request, 'authentication/set_newpassword.html', context)
        if len(password) < 6:
            messages.error(request, 'Password too short')
            return render(request, 'authentication/set_newpassword.html', context)
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password saved successfully login in now')
            return redirect('login')
        except Exception as identifier:
            messages.info(request, "Something went wrong")
            return render(request, 'authentication/set_newpassword.html', context)


        

        
                
            

        