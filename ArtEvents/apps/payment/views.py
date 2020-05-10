import json
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import *
from django.views.decorators.http import require_POST, require_GET
from apps.dashboard.autoreply import payreply
from apps.dashboard.autoreply import canelreply


def payment(request):
    eid = request.GET.get('eid')
    price = TicketHas.objects.filter(eid = eid).values('price')[0].get('price')
    refund = TicketHas.objects.filter(eid=eid).values('refund_policy')[0].get('refund_policy')
    if refund == "yes":
        refund = "As you wish"
    elif refund == "no":
        refund = "No Refund"
    content = {
        'eid' : eid,
        'price' : price,
        'refund': refund
    }
    return render(request, 'Payment.html', context = {'content' : content})

@csrf_exempt
def write_pay_info(request):
    thisId = request.POST.get('eid', None) ## 获取EID
    t_num = request.POST.get('ticketnum', None) ## 获取票的张数
    ticket = TicketHas.objects.get(eid=thisId)
    all_num = ticket.amount
    new_num = int(all_num) - int(t_num)
    TicketHas.objects.filter(eid=thisId).update(amount=str(new_num))
    cname = request.POST.get('credit-number', None) # credit card number
    address = request.POST.get('address', None) # address
    email = request.POST.get('email', None)
    fname = request.POST.get('fname', None) # first name
    lname = request.POST.get('lname', None) # last name
    ticket_price = TicketHas.objects.filter(eid=thisId).values('price')[0].get('price')
    total_price = int(t_num) * int(ticket_price)
    dic1 = {'pid': str(cname), 'address': str(address), 'fname': str(fname), 'lname': str(lname), 'ticket_num': str(t_num), 'total_price': str(total_price), 'email': str(email)}
    print('form', dic1)
    Payment.objects.create(**dic1)
    content = {
        'fname': fname,
        'lname': lname,
        'address': address,
        'total_price': total_price
    }
    emailTo = email
    payId = str(cname)
    payreply(emailTo, payId)
    return render(request, 'TransactionSuccessPage.html', context={'content': content})

@require_GET
def get(request):
    return render(request, 'CancelOrder.html')

@csrf_exempt
@require_POST
def cancel(request):
    print(request.method)
    info = json.loads(request.body)
    print(info)
    payId = info.get('pid')
    emailTo = Payment.objects.get(pid=payId).email
    money = Payment.objects.get(pid=payId).total_price
    canelreply(emailTo, money)
    Payment.objects.get(pid=payId).delete()
    confirmation = "You've successfully cancelled your order!"
    return HttpResponse(confirmation)