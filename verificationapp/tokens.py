from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.contrib.sites.shortcuts import get_current_site

def send_mail_after_registration(email, token, username, request):
    subject = "Your account needs to be verified"
    # message = f'''Hi paste your link to verify your account <p><a href="https://yourwebsite.com/verify?token=xyz123">Verify Email</a></p> http://127.0.0.1:8000/verify/{token}
   
    # '''
    message = render_to_string('gmail_verification_link.html', {
        'user': username,
        'domain': get_current_site(request).domain, 
        'token': token,
        "protocol": 'https' if request.is_secure() else 'http'
    })
    print(message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list)

    print("all is good")