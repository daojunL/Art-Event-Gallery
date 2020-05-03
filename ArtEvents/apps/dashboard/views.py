from dashboard.models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.mail import send_mail
import datetime
import json
from django.conf import settings
from apps.dashboard.autoreply import autoreply
from django.views.decorators.http import require_POST, require_GET
from music import views as musicViews

@require_GET
def home(request):
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
        addr = Location.objects.filter(lid=lid[0].get('lid')).values('address')
        address.append(musicViews.formatAddr(addr[0].get('address')))

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
    #end = datetime.datetime.now()
    #print((end - start))
    return render(request, 'HomePage.html', context=content)

def detail(request):
    eid = request.GET['eid']

    title = ArtEvents.objects.filter(eid = eid).values('title')[0].get('title')
    aid = Perform.objects.filter(eid = eid).values('aid')[0].get('aid')
    name = Artist.objects.filter(aid = aid).values('artist_name')[0].get('artist_name')
    seatmap = ArtEvents.objects.filter(eid=eid).values('seatmap')[0].get('seatmap')
    lid = Held.objects.filter(eid=eid).values('lid')[0].get('lid')
    address = musicViews.formatAddr(Location.objects.filter(lid=lid).values('address')[0].get('address')) # address这里还要对数据进行进一步的处理
    timeSerial = TOn.objects.filter(eid=eid).values('time_serial')[0].get('time_serial')
    date = Time.objects.filter(time_serial=timeSerial).values('date_ymd')[0].get('date_ymd')
    content = {
        'eid':eid,
        'title': title,
        'name':name,
        'seatmap':seatmap,
        'address':address,
        'date':date
    }
    return render(request, 'EventPage.html', context = {'content': content})

@require_GET
def ContactPage(request):
    return render(request, 'ContactPage.html')

@csrf_exempt
@require_POST
def subscribe(request):
    info = json.loads(request.body)
    name = info.get('name')
    emailTo = info.get('email')
    # add data
    sid = emailTo +"123"
    dict = {'sid':sid, 'email':emailTo, 's_name':name}
    Subscription.objects.create(**dict)

    # Autoreply.
    autoreply(emailTo)
    confirmation = "Thanks for subscribing!"
    return HttpResponse(confirmation)
