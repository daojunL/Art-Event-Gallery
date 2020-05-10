import json
from django.views.decorators.http import require_POST, require_GET
from django.http import Http404
from audioop import reverse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import *
import datetime, pytz
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.

class Event:

    def __init__(self, eid, title, e_image, date, address):
        self.eid = eid
        self.title = title
        self.e_image = e_image
        self.date = date
        self.address = address


@require_GET
# Create your views here.
def ShowEvents(request):
    """the music search page"""
    # return 8 events:{'Eid':[title, e_image, address, date_YMD]}
    eids = Theater.objects.all()[:8].values('eid')
    event0 = ArtEvents.objects.filter(eid=eids[0].get('eid'))[0]
    event1 = ArtEvents.objects.filter(eid=eids[1].get('eid'))[0]
    event2 = ArtEvents.objects.filter(eid=eids[2].get('eid'))[0]
    event3 = ArtEvents.objects.filter(eid=eids[3].get('eid'))[0]
    event4 = ArtEvents.objects.filter(eid=eids[4].get('eid'))[0]
    event5 = ArtEvents.objects.filter(eid=eids[5].get('eid'))[0]
    event6 = ArtEvents.objects.filter(eid=eids[6].get('eid'))[0]
    event7 = ArtEvents.objects.filter(eid=eids[7].get('eid'))[0]
    selectEvents = [event0, event1, event2, event3, event4, event5, event6, event7]
    print(selectEvents)
    eid = [x.eid for x in selectEvents]
    title = [x.title for x in selectEvents]
    e_image = [x.e_image for x in selectEvents]
    address = []
    date_YMD = []
    for item in eid:
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
    events = []

    for i in range(len(content['Eid'])):
        events.append(Event(content['Eid'][i], content['title'][i], content['e_image'][i], content['date'][i], content['address'][i]))

    return render(request, 'SearchTheaterPage.html', context={'events': events})

@csrf_exempt
@require_POST
def QueryEvents(request):
    # post method
    timeDict = {'1': 7,
                '2': 30,
                '3': 90,
                '4': 180,
                '5': 365}
    city = request.POST.get('city', None)
    time = request.POST.get('time', None)
    type = request.POST.get('type', None)

    if time == "In a week":
        time = "1"
    elif time == "In a month":
        time = "2"
    elif time == "In three months":
        time = "3"
    elif time == "In half a year":
        time = "4"
    elif time == "In a year":
        time = "5"
    else:
        time = ''

    if city == "default":
        city = ""

    if type == "default":
        type = ""

    print(city)
    print(time)
    print(type)
    # find the search eventid
    Eid1, Eid2, Eid3 = set(), set(), set()
    if city != '':
        lid = Location.objects.filter(address__contains=city).values('lid')
        # if len(lid) == 0:
        #     pass
        # return render(request, 'SearchConcertPage.html', {'error_message':'Events not found'})
        if len(lid) == 1:
            curlid = lid[0].get('lid')
            eid = Held.objects.filter(lid=curlid).values('eid')
            Eid1.add(eid[0].get('eid'))
        else:
            for i in range(len(lid)):
                curlid = lid[i].get('lid')
                eid = Held.objects.filter(lid=curlid).values('eid')
                Eid1.add(eid[0].get('eid'))
    else:
        tmpEvents = ArtEvents.objects.all().values('eid')
        for i in range(len(tmpEvents)):
            Eid1.add(tmpEvents[i].get('eid'))

    if time != '':
        Timedata = Time.objects.values()
        setDate = datetime.date(2020, 4, 20)  # set a date
        for i in range(len(Timedata)):
            # date = datetime.datetime(Timedata[i].get('Tyear'),Timedata[i].get('Tmonth'),(Timedata[i].get('Tday')))
            date = datetime.date.fromisoformat(Timedata[i].get('date_ymd'))

            interval = date - setDate
            if interval.days < timeDict[time]:
                curtSerial = Timedata[i].get('time_serial')
                eid = TOn.objects.filter(time_serial=curtSerial).values('eid')
                Eid2.add(eid[0].get('eid'))
    else:
        tmpEvents = ArtEvents.objects.all().values('eid')
        for i in range(len(tmpEvents)):
            Eid2.add(tmpEvents[i].get('eid'))


    if type != '':
        eid = Theater.objects.filter(genre__contains=type).values('eid')
        print("test")
        print(eid)
        for i in range(len(eid)):
            Eid3.add(eid[i].get('eid'))
    else:
        tmpEvents = ArtEvents.objects.all().values('eid')
        for i in range(len(tmpEvents)):
            Eid3.add(tmpEvents[i].get('eid'))

    # get the intersection of Eid1 / Eid2 / Eid3
    finalEid = Eid1 & Eid2 & Eid3
    eid = list(finalEid)
    ## query: Eid, title, e_image，address, date_YMD
    title, e_image, address, date_YMD = [], [], [], []
    print("finalEid")
    print(len(finalEid))
    if len(finalEid) == 0:
        content = {
            'status': 'FAILED'
        }
        # return render(request, 'SearchConcertPage.html', context=content)
        return JsonResponse(content)
    else:
        for item in finalEid:
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
        'eid': eid,
        'title': title,
        'e_image': e_image,
        'address': address,
        'date': date_YMD,
        'status': 'SUCCESS'
    }
    # sort by date desc
    content['date'].sort()
    # sort by distance
    # if sort == "2":

    events = []

    for i in range(len(content['eid'])):
        events.append(Event(content['eid'][i], content['title'][i], content['e_image'][i], content['date'][i],
                            content['address'][i]))

    return render(request, 'SearchTheaterPage.html', context={'events': events})




