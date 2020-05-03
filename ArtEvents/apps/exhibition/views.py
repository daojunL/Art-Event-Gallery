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

@require_GET
# Create your views here.
def ShowEvents(request):
    """the music search page"""
    # return 8 events:{'Eid':[title, e_image, address, date_YMD]}
    eids = Exhibition.objects.all()[:8].values('eid')
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
        addr = Location.objects.filter(lid=lid[0].get('lid')).values('address')
        address.append(addr[0].get('address'))
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
    content['date'].sort()
    return render(request, 'SearchExhibitionPage.html', context={'content': content})

@csrf_exempt
@require_POST
def QueryEvents(request):
    # post method
    timeDict = {'1': 7,
                '2': 30,
                '3': 90,
                '4': 180,
                '5': 365}
    data = json.loads(request.body)
    city = data.get('City')
    time = data.get('Time')
    type = data.get('Type')
    sort = data.get('Sort')
    print("city")
    print(city)
    print("time")
    print(time)
    print("type")
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


    print("eid1")
    print(Eid1)
    print("eid2")
    print(Eid2)
    print("eid3")
    print(Eid3)
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
    elif len(finalEid) == 1:
        feid = finalEid[0]
        t = ArtEvents.objects.filter(eid=feid).values('title', 'e_image')  # title, e_image
        title.append(t[0].get('title'))
        e_image.append(t[0].get('e_image'))

        lid = Held.objects.filter(eid=feid).values('lid')
        addr = Location.objects.filter(lid=lid[0].get('lid')).values('address')
        address.append(addr[0].get('address'))  # address

        timeSerial = TOn.objects.filter(eid=feid).values('time_serial')
        date = Time.objects.filter(time_serial=timeSerial[0].get('time_serial')).values('date_ymd')
        date_YMD.append(date[0].get('date_ymd'))
    else:
        for item in finalEid:
            t = ArtEvents.objects.filter(eid=item).values('title', 'e_image')  # title, e_image

            title.append(t[0].get('title'))
            e_image.append(t[0].get('e_image'))

            lid = Held.objects.filter(eid=item).values('lid')
            addr = Location.objects.filter(lid=lid[0].get('lid')).values('address')
            address.append(addr[0].get('address'))

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
    return JsonResponse(content)

def detail(request):
    eid = request.GET['eid']
    print("exhibition")
    print(eid)
    title = ArtEvents.objects.filter(eid = eid).values('title')[0].get('title')
    print(title)
    background = Exhibition.objects.filter(eid=eid).values('background')[0].get('background')
    print(background)
    lid = Held.objects.filter(eid=eid).values('lid')[0].get('lid')
    print(lid)
    address = Location.objects.filter(lid=lid).values('address')[0].get('address') # address这里还要对数据进行进一步的处理
    print(address)
    timeSerial = TOn.objects.filter(eid=eid).values('time_serial')[0].get('time_serial')
    print(timeSerial)
    date = Time.objects.filter(time_serial=timeSerial).values('date_ymd')[0].get('date_ymd')
    print(date)
    content = {
        'eid':eid,
        'title': title,
        'background':background,
        'address':address,
        'date':date
    }
    return render(request, 'EventPage2.html', context = {'content': content})

