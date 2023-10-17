import uuid 
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from .forms import LoginForm, CustomUserCreationForm
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
from django.core.exceptions import ObjectDoesNotExist

def login_attempt(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username =  cleaned_data['username']
            password = cleaned_data['password']
            print(form.errors, "error")
        if form.errors:
            print(1)
            messages.success(request,f'{form.errors}')
            return redirect('/login')
        try:
            print(2)
            user = User.objects.filter(username=username).first()    
            if user is None:
                messages.success(request,'Bunday user mavjud emas')
            else:  
                profile_obj = Profile.objects.get(user=user.id)
                if profile_obj and profile_obj.is_verified == True:
                    print(3)
                    # user = User.objects.get(username=username)
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        print(4)
                        login(request, user)
                        return redirect('/')
                    else:
                        messages.success(request,'Parol mos kelmadi')
                else:
                    messages.success(request, "Akkount tasdiqlanmagan, gmail orqali tasdiqlang")
        except Exception as e:
            print(e)
    return render (request, 'login.html')


def register_attempt (request):
        if request.method == 'POST' :
            form = CustomUserCreationForm(request.POST)
            if form.errors:
                messages.success(request, f'{form.errors}') 
                return redirect('/register')
            elif form.is_valid():
                username = request.POST.get('username')
                email = request.POST.get('email')
                try:
                    if username == None:
                        messages.success(request, 'username maydoni bo\'sh  bo\'lishi mumkin emas.') 
                        return redirect('/register')
                    elif email == None:
                        messages.success(request, 'email maydoni bo\'sh  bo\'lishi mumkin emas.') 
                        return redirect('/register')
                    elif User.objects.filter(username = username).first():
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




    