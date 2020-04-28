from django.shortcuts import render
from dashboard.models import *
from django.core.mail import send_mail
import json
from django.conf import settings
from django.views import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from dashboard.autoreply import autoreply


# Create your views here.
def home(request):
    """the homepage view"""
    return render(request, 'HomePage.html')


class ContactPage(View):
    def get(self, request):
        return render(request, 'ContactPage.html')

    @csrf_exempt
    def post(self, request):
        if request.POST:
            title = "Contact"
            confirmation = None
            info = json.loads(request.body)
            name = info.get('name')
            emailTo = info.get('email')
            print(name)
            print(emailTo)

            emailsub = name + " successfully subscribe to our website"
            emailmessage = 'Dear %s user email: %s' % (name, emailTo)
            emailFrom = [settings.EMAIL_HOST_USER]
            send_mail(emailsub, emailmessage, emailFrom, list(emailTo), fail_silently=True)
            # Autoreply.
            autoreply(emailTo)
            confirmation = "Thanks for subscribing!"
            return HttpResponse(confirmation)

# def subscribe(request):
#     if request.POST:
#         title = "Contact"
#         confirmation = None
#         info = json.loads(request.body)
#         name = info.get('name')
#         emailTo = info.get('email')
#         print(name)
#         print(emailTo)
#
#         emailsub = name + " successfully subscribe to our website"
#         emailmessage = 'Dear %s user email: %s' % (name, emailTo)
#         emailFrom = [settings.EMAIL_HOST_USER]
#         send_mail(emailsub, emailmessage, emailFrom, list(emailTo), fail_silently=True)
#         # Autoreply.
#         #autoreply.autoreply(emailFrom)
#         confirmation = "Thanks for subscribing!"
#         return render(request, 'ContactPage.html', "Thanks for subscribing!")
