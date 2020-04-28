import json
from audioop import reverse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import *
import datetime, pytz
from django.http import HttpResponseRedirect
# from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.

@csrf_exempt
def theaterPage(request):
    if request.GET:
        # return 8 events:{'Eid':[title, e_image, address, date_YMD]}
        selectEvents = ArtEvents.objects.all()[:8]
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
        return render(request, 'SearchTheaterPage.html', context=content)

# ajax
def QueryTheater(request):
    """the music search page"""
    # if request.method == "GET":
    #     return render(request, 'SearchConcertPage.html')
    if request.POST:
        timeDict = {'1': 7,
                    '2': 30,
                    '3': 90,
                    '4': 180,
                    '5': 365}
        data = json.loads(request.body)
        city = data.get('City')
        time = data.get('Time')
        type = data.get('Type')


        # find the search eventid
        Eid1, Eid2, Eid3 = set(), set(), set()
        if city != '':
            lid = Location.objects.filter(address__contains=city).values('Lid')
            # if len(address_id) == 0:
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
                    Eid2.add(eid[0].get('Eid'))
        else:
            tmpEvents = ArtEvents.objects.all().values('eid')
            for i in range(len(tmpEvents)):
                Eid2.add(tmpEvents[i].get('eid'))

        if type != '':
            eid = Theater.objects.filter(genre__contains=type).values('eid')
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
            'Eid': eid,
            'title': title,
            'e_image': e_image,
            'address': address,
            'date': date_YMD,
            'status': 'SUCCESS'
        }
        # sort by date desc
        content['date'].sort()
        return JsonResponse(content)


def sortbyDate(request):
    # select top 8 events from all events
    if request.POST:
        eid, title, e_image, address, date_YMD = [], [], [], [], []
        orderData = Time.objects.all().order_by('date_ymd')[:8]
        for i in range(len(orderData)):
            timeSerial = orderData[i].time_serial
            tmpEid = TOn.objects.filter(time_serial=timeSerial).values('eid')
            Eid = tmpEid[0].get('eid')
            eid.append(Eid)

            t = ArtEvents.objects.filter(eid=Eid).values('title', 'e_image')  # title, e_image
            title.append(t[0].get('title'))
            e_image.append(t[0].get('e_image'))

            lid = Held.objects.filter(eid=Eid).values('lid')
            addr = Location.objects.filter(lid=lid[0].get('lid')).values('address')
            address.append(addr[0].get('address'))

            timeSerial = TOn.objects.filter(eid=Eid).values('time_serial')
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
        # sort by date desc
        content['date'].sort()
        return render(request, 'SearchTheaterPage.html', context=content)


# def sortbyDistance(request):
#     if request.POST:

# class QueryMusic(View):
#     def get(self, request):
#         # if get, return to default page
#         return HttpResponseRedirect(reverse(musicPage))
#
#     def post(self, requst):
#         if request.POST.get('confirm'):


def theater_details(request):
    if request.POST:
        data = json.loads(request.body)
        Eid = data.get('Eid')
        s = ArtEvents.objects.filter(eid=Eid).values('seatmap')
        seatmap = s[0].get('seatmap')

        aid = Perform.objects.filter(eid=Eid).values('aid')
        p = Artist.objects.filter(aid=aid[0].get('aid')).values('artist_name')
        performers = p[0].get('artist_name')

        timeSerial = TOn.objects.filter(eid=Eid).values('time_serial')
        date = Time.objects.filter(time_serial=timeSerial[0].get('time_serial')).values('date_ymd')
        time = date[0].get('date_ymd')

        lid = Held.objects.filter(eid=Eid).values('lid')
        addr = Location.objects.filter(lid=lid[0].get('lid')).values('address')
        location = addr[0].get('address')

        content = {
            'Eid': Eid,
            'seatmap': seatmap,
            'performers': performers,
            'address': location,
            'time': time
        }
        return render(request, 'EventPage.html', context=content)

