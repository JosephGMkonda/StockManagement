from .views import RegistrationView,UsernameValidationView,EmailValidationView,VerificationView,LoginView,LogoutView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns =[

    path('register',csrf_exempt(RegistrationView.as_view()),name="register"),
    path('login',csrf_exempt(LoginView.as_view()),name="login"),
    path('logout', csrf_exempt(LogoutView.as_view()),name="logout"),
    path('username_validation',csrf_exempt(UsernameValidationView.as_view()),name='username_validation'),
    path('email_validation',csrf_exempt(EmailValidationView.as_view()),name='email_validation'),
    path('verification/<uidb64>/<token>',csrf_exempt(VerificationView.as_view()), name="verification")
]