from django.shortcuts import render, redirect
from .forms import LoginForm

def home (request):
    return render (request , 'home.html')
from django.contrib.auth import authenticate, login
def login_attempt(request):
    print(request.method, "\n\n\n\n")
    form = LoginForm(request.POST)
    print(form.is_valid, "form valid or invalid", form.errors)
    if request.method == "POST":
        print("True1")
        # if form.
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # email = request.POST.get('email')
        # password = request.POST.get('password')
        print(username)
        user = User.objects.get(username=username)
        print(password)
        print(user.password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # The password is correct
            login(request, user)
            return redirect('/')
        # if password==user.password:
        #     print("redirected")
        #     return redirect('/')
        else:
            messages.success(request,'password is error ekan')
    return render (request, 'login.html')

from .models import Profile
import uuid
from django.contrib.auth import get_user_model
from django.contrib import messages
User = get_user_model()
from django.contrib.auth.hashers import make_password

from .forms import CustomUserCreationForm
def register_attempt (request):
        print(request.method, "\n\n\n\n\n\n")
        if request.method == 'POST' :
            form = CustomUserCreationForm(request.POST)
            print("Form is ", form.is_valid(), form.errors)
            if form.is_valid():
                username = request.POST.get('username')
                email = request.POST.get('email')
                password = request.POST.get('password')
                try:
                    if User.objects.filter(username = username).first():
                        messages.success(request,'Username is taken.')
                        return redirect('/register')

                    elif User.objects.filter(email = email).first():
                        messages.success(request, 'Email is taken')
                        return redirect('/register')
                    # user_obj = User.objects.create(username = username, email=email, password=make_password(password) )
                    # # user_obj.set_password(password)
                    # print(make_password(password))
                    # print(user_obj.set_password(password))
                    form.save()
                    # user_obj.save()
                    token = str(uuid.uuid4)
                    user_obj = User.objects.get(email=email)
                    profile_obj = Profile.objects.create(user = user_obj , auth_token = token)
                    profile_obj.save()
                    send_mail_after_registration(email=email, token=token )

                    return redirect('/token')
                except Exception as e:
                    print(e)
            return redirect('/login/')
            # username = request.POST.get('username')
            # email = request.POST.get('email')
            # password = request.POST.get('password')

            try:
                if User.objects.filter(username = username).first():
                    messages.success(request,'Username is taken.')
                    return redirect('/register')

                elif User.objects.filter(email = email).first():
                    messages.success(request, 'Email is taken')
                    return redirect('/register')

                user_obj = User.objects.create(username = username, email=email, password=make_password(password) )
                # user_obj.set_password(password)
                print(make_password(password))
                print(user_obj.set_password(password))
                # user_obj.save()
                token = str(uuid.uuid4)
                profile_obj = Profile.objects.create(user = user_obj , auth_token = token)
                profile_obj.save()
                send_mail_after_registration(email=email, token=token )

                return redirect('/token')

            except Exception as e:
                print(e)

        return render(request , 'register.html')

def token_send (request):
    return render(request , 'token_send.html')

def success (request):
    return render(request , 'success.html')


def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'You account is been verified')
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)


def error_page(request):
    return render(request, 'error.html')   

from django.conf import settings
from django.core.mail import send_mail
def send_mail_after_registration(email,token):
    subject = "Your account needs to be verified"
    message = f'Hi paste your link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list)
    print("all is good")
    