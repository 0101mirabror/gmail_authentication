from django.shortcuts import render, redirect
import uuid
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .forms import CustomUserCreationForm
from .models import Profile
from .tokens import send_mail_after_registration

User = get_user_model()



def home (request):
    return render (request , 'home.html')


def token_send (request):
    return render(request , 'token_send.html')


def success (request):
    return render(request , 'success.html')


def error_page(request):
    return render(request, 'error.html')   


def login_attempt(request):
    print(request.method, "\n\n\n\n LOGIN")
    form = LoginForm(request.POST)
    print(form.is_valid, "form valid or invalid", form.errors)
    if request.method == "POST":
        print("True1")
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        try:
            print(1)
            user = User.objects.get(username=username)
            profile_obj = Profile.objects.get(user=user.id)
            print(profile_obj)
            if profile_obj and profile_obj.is_verified == True:
                print(3)
                print(username)
                user = User.objects.get(username=username)
                print(password)
                print(user.password)
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')
                else:
                    messages.success(request,'Parol mos kelmadi')
        except Exception as e:
            print(e)
    return render (request, 'login.html')



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
                    form.save()
                    token = str(uuid.uuid4)
                    user_obj = User.objects.get(email=email)
                    profile_obj = Profile.objects.create(user = user_obj , auth_token = token)
                    profile_obj.save()
                    print("Salom")
                    send_mail_after_registration(email=email, token=token, request=request, username=username)
                    return redirect('/token')
                except Exception as e:
                    print(e)
            return redirect('/register/')
        return render(request , 'register.html')


def verify(request ,  token):
    try:
        profile_obj = Profile.objects.filter(auth_token = token).first()
        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'You account is been verified')
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)




    