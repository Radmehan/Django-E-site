from ast import Or
from cgitb import reset
from os import stat
from turtle import update
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json


# Create your views here.
def index(request):
    # products = Product.objects.all()
    # n = len(products)
    # nSlides = n//4 + ceil((n/4) - (n//4))
    # params = {'product':products,'no_of_slides':nSldies,'range':(1,nSldies)}
    # allProds=[[products,range(1,nSlides),nSlides],[products,range(1,nSlides),nSlides]]
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item["category"] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4) - (n//4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params={'allProds':allProds}
    return render(request,"shop/index.html",params)


def about(request):
    return render(request,"shop/about.html")


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        contact = Contact(name=name, email=email, phone=phone, msg=message)
        contact.save()
    return render(request,"shop/contact.html")


def tracker(request):
    if request.method == 'POST':
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order=Order.objects.filter(order_id=orderId, email=email)
            if(order(len)>0):
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response = json.dumps([updates,order[0].items_json], default=str)
                return HttpResponse(response)

            else:
               return HttpResponse('{}')

        except Exception as e:
           return HttpResponse('{}')

    return render(request,"shop/tracker.html")


def prodView(request,myid):
    # fetch the product using the id
    product = Product.objects.filter(id=myid)
    print(product)
    return render(request,"shop/prodView.html", {'product' : product[0]})


def search(request):
    return render(request,"shop/search.html")


def checkout(request):
    if request.method == 'POST':
        itemsJson = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') +" "+ request.POST.get('address2', '')
        city = request.POST.get('city', '')
        zip = request.POST.get('zip_code', '')
        state = request.POST.get('state', '')
        phone = request.POST.get('phone', '')
        order = Order(items_json=itemsJson, name=name, email=email, address=address, city=city, zip_code=zip, state=state ,phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request,"shop/checkout.html",{'thank':thank, 'id':id})
    return render(request,"shop/checkout.html")