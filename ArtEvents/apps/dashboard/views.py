from dashboard.models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.mail import send_mail
import json
from django.conf import settings
from apps.dashboard.autoreply import autoreply
# Create your views here.
from django.views.decorators.http import require_POST, require_GET

@require_GET
def home(request):
    """the homepage view"""
    return render(request, 'HomePage.html')

@require_GET
def get(request):
    return render(request, 'ContactPage.html')

@csrf_exempt
@require_POST
def post(request):
    print(request.method)
    info = json.loads(request.body)
    print(info)
    name = info.get('name')
    emailTo = info.get('email')
    emailsub = name + " successfully subscribe to our website"
    emailmessage = 'Dear %s user email: %s' % (name, emailTo)
    emailFrom = settings.EMAIL_HOST_USER
    send_mail(emailsub, emailmessage, emailFrom, [emailTo], fail_silently=True)
    # Autoreply.
    autoreply(emailTo)
    confirmation = "Thanks for subscribing!"
    return HttpResponse(confirmation)
