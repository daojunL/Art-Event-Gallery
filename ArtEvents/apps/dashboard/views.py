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
    """the homepage view"""
    # 4 events per category
    #start = datetime.datetime.now()
    eid,title, e_image, address, date_YMD = [], [], [], [], []
    mId = Concert.objects.all().values('eid')[:4]  # concert
    tId = Theater.objects.all().values('eid')[:4]  # theater
    eId = Exhibition.objects.all().values('eid')[:4]  # exhibition
    for i in range(len(mId)):
        eid.append(mId[i].get('eid'))
        eid.append(tId[i].get('eid'))
        eid.append(eId[i].get('eid'))
    for item in eid:
        t = ArtEvents.objects.filter(eid=item).values('title', 'e_image')  # title, e_image
        title.append(t[0].get('title'))
        e_image.append(t[0].get('e_image'))
        lid = Held.objects.filter(eid=item).values('lid')
        addr = Location.objects.filter(lid=lid[0].get('lid')).values('address')[0].get("address")
        address.append(addr.split("/")[1])
        timeSerial = TOn.objects.filter(eid=item).values('time_serial')
        date = Time.objects.filter(time_serial=timeSerial[0].get('time_serial')).values('date_ymd')
        date_YMD.append(date[0].get('date_ymd'))

    content = {
        'Eid': eid,
        'title': title,
        'e_image': e_image,
        'address': address,
        'date': date_YMD,
        'status': 'SUCCESS'
    }

    return render(request, 'HomePage.html', context={'content': content})

@require_GET
def get(request):
    return render(request, 'ContactPage.html')

@csrf_exempt
@require_POST
def subscribe(request):
    info = json.loads(request.body)
    print("hello")
    name = info.get('name')
    emailTo = info.get('email')
    print(emailTo)
    # add data
    sid_data = getattr(Subscription.objects.last(), 'sid')
    sid = str(int(sid_data) + 1)
    dict = {'sid':sid, 'email':emailTo, 's_name':name}
    Subscription.objects.create(**dict)
    # Autoreply.
    autoreply(emailTo)
    confirmation = "Thanks for subscribing!"
    return HttpResponse(confirmation)
