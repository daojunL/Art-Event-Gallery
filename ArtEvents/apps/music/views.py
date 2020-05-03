import json
from django.views.decorators.http import require_POST, require_GET
from django.http import Http404
from audioop import reverse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import *
import pytz, datetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
import re
# Create your views here.

@require_GET
# Create your views here.
def formatAddr(str):
    newStr1 = str.replace("/",",")
    newStr2 = re.sub(",time_zone:America,New_York", " ", newStr1).strip()
    return newStr2

def MusicPage(request):
    """the music search page"""
    # return 8 events:{'Eid':[title, e_image, address, date_YMD]}
    # start = datetime.datetime.now()
    eid, title, e_image, address, date_YMD = [], [], [], [], []
    mId = Concert.objects.all().values('eid')[:8]  # concert
    for i in range(len(mId)):
        eid.append(mId[i].get('eid'))
    for item in eid:
        t = ArtEvents.objects.filter(eid=item).values('title', 'e_image')  # title, e_image

        title.append(t[0].get('title'))
        e_image.append(t[0].get('e_image'))

        lid = Held.objects.filter(eid=item).values('lid')
        addr = Location.objects.filter(lid=lid[0].get('lid')).values('address')
        address.append(formatAddr(addr[0].get('address')))

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
    # end = datetime.datetime.now()
    # print((end - start))

    return render(request, 'SearchConcertPage.html', context={'content': content})

@csrf_exempt
@require_POST
def MusicQuery(request):
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
    # city = 'Boston'
    # time = '5'
    # type = 'Rock'
    # start = datetime.datetime.now()
    # find the search eventid
    Eid1, Eid2, Eid3 = set(), set(), set()
    tmpEid = set()
    tmpEvents = ArtEvents.objects.all().values('eid')
    for i in range(len(tmpEvents)):
        tmpEid.add(tmpEvents[i].get('eid'))
    if city != '':
        lid = Location.objects.filter(address__contains=city).values('lid')
        if len(lid) == 0:
        #     pass
            return render(request, 'SearchConcertPage.html', {'error_message':'Events not found'})
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
        Eid1 = tmpEid


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
        Eid2 = tmpEid


    if type != '':
        eid = Concert.objects.filter(concert_type__contains=type).values('eid')
        for i in range(len(eid)):
            Eid3.add(eid[i].get('eid'))
    else:
        Eid3 = tmpEid

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
        # pass
    elif len(finalEid) == 1:
        feid = finalEid[0]
        t = ArtEvents.objects.filter(eid=feid).values('title', 'e_image')  # title, e_image
        title.append(t[0].get('title'))
        e_image.append(t[0].get('e_image'))

        lid = Held.objects.filter(eid=feid).values('lid')
        addr = Location.objects.filter(lid=lid[0].get('lid')).values('address')
        address.append(formatAddr(addr[0].get('address'))) # address

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
            address.append(formatAddr(addr[0].get('address')))

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
    # end = datetime.datetime.now()
    # print(end - start)

    return JsonResponse(content)


def payment(request):
    eid = request.GET.get('eid')
    price = TicketHas.objects.filter(eid = eid).values('price')[0].get('price')
    content = {
        'eid' : eid,
        'price' : price
    }
    return render(request, 'Payment.html', context = {'content' : content})

@csrf_exempt
def write_pay_info(request):
    thisId = request.POST.get('eid', None) ## 获取EID
    t_num = request.POST.get('ticketnum', None) ## 获取票的张数
    ticket = TicketHas.objects.get(eid=thisId)
    print(ticket)
    all_num = ticket.amount
    new_num = int(all_num) - int(t_num)
    print('n', new_num)
    TicketHas.objects.filter(eid=thisId).update(amount=str(new_num))
    cname = request.POST.get('credit-number', None) # credit card number
    address = request.POST.get('address', None) # address
    fname = request.POST.get('fname', None) # first name
    lname = request.POST.get('lname', None) # last name
    ticket_price = TicketHas.objects.filter(eid=thisId).values('price')[0].get('price')
    total_price = int(t_num) * int(ticket_price)
    dic1 = {'pid': str(cname), 'address': str(address), 'fname': str(fname), 'lname': str(lname), 'ticket_num': str(t_num), 'total_price': str(total_price)}
    print('form', dic1)
    Payment.objects.create(**dic1)
    content = {
        'fname': fname,
        'lname': lname,
        'address': address,
        'total_price': total_price
    }
    return render(request, 'TransactionSuccessPage.html', context = {'content': content})
