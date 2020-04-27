from django.shortcuts import render
from .models import *
from django.core.mail import send_mail
import json
from django.conf import settings
from dashboard.autoreply import autoreply


# Create your views here.
def home(request):
    """the homepage view"""
    return render(request, 'HomePage.html')

def subscribe(request):
    if request.POST:
        title = "Contact"
        confirmation = None
        info = json.loads(request.body)
        email = info.get('email')
        fix = info.get('fix')
        lname = info.get('lastName')

        emailsub = lname + " successfully subscribe to our website"
        emailmessage = '%s %s user email: %s' % (fix, lname, emailFrom)
        emailTo = [settings.EMAIL_HOST_USER]
        send_mail(emailsub, emailmessage, list(emailTo), fail_silently=True)
        # Autoreply.
        autoreply.autoreply(emailFrom)
        title = "Thanks."
        confirmation = "We will get right back to you."
        form = None

        context = {'title': title, 'form': form, 'confirmation': confirmation, }
        template = 'HomePage.html'
        return render(request, template, context)






