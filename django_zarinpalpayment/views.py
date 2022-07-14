from email import header
from os import stat
import zoneinfo
from django.shortcuts import render, redirect
from django.views import generic
from requests import head
import requests
from .config import zconfig
from zeep import Client

client = Client(zconfig.payment_request)
amount = 10000
email = 'none@gmail.com'
phone = "09123456789"

# Create your views here.
class ZarinpalSendRequest(generic.View):
    def get(self, request): 
        return render(request, 'payment.html', {})

    def post(self, request):
        description = "This is a test description"

        result = client.service.PaymentRequest(zconfig.merchant_id, amount, description, email, phone, zconfig.payment_callback)

        print(result)

        if not result.Status == 100:
            return render(request, 'error_page.html', {'result': "Transaction failed or canceled by user."})
        return redirect(zconfig.payment_startpay.format(authority=result.Authority))
        # print(result)



class ZarinPalVerifyView(generic.View):
    def get(self, request):
        status = request.GET.get("Status")
        authority = request.GET['Authority']
        if status == 'OK':
            
            result = client.service.PaymentVerification(zconfig.merchant_id, authority, amount)
            
            if result.Status == 100 or result.Status == 101:
                return render(request, 'done.html', {'result': str(result.RefID)})
            return render(request, 'error_page.html', {'result': result})
        else:
            return render(request, 'error_page.html', {'result': 'Transaction failed or canceled by user'})

              
