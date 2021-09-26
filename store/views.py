from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from .models import *
from django.http import JsonResponse
import json
import datetime
from . utils import cookieCart, cartData, guestOrder
# from django.core.mail import send_mail
# from django.conf import settings

# Create your views here.

# price_1ICV7qBBFg9oIquvaWQhDmqP


def home(request):
    # return HttpResponse(" YO")
    return render(request, 'store/home.html')


def main(request):
    context = {}
    # return HttpResponse(" YO")
    return render(request, 'store/main.html', context)

# def product.id(request):
    

def shop(request):

    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {"products": products, 'cartItems': cartItems}
    return render(request, 'store/shop.html', context)


def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def productdetails(request,id):
    product = Product.objects.get(id=id)
    return render(request,'store/productId.html',{'product':product})

# def email(request):
    
#     if request.method=="POST":
#         message = request.POST['message']
        
#         send_mail('Contact form',
#                 message,
#                 settings.EMAIL_HOST_USER,
#                 ['email'],
#                 fail_silently=False)
#         return render(request, 'store/cart.html')


    # stripe.api_key =settings.STRIPE_PRIVATE_KEY

    # stripe.checkout.Session.create(
    #     success_url="https://example.com/success",
    #     cancel_url="https://example.com/cancel"
    #     payment_method_types=["card"],
    #     line_items=[
    #         {
    #         "price": "price_H5ggYwtDq4fbrJ",
    #         "quantity": 2,
    #         },
    #     ],
    #     mode="payment",
    # )


def checkout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added ', safe=False)

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# @csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print('Data:', request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],

        )
        
    #EMAIL ATTEMPT 
    # if order.shipping == True:
    #     template = render_to_string('store/tyemail.html' , {'name': request.user.first_name})
        
    #     email = EmailMessage (
    #         'subject'
    #         'body',
    #         settings.EMAIL_HOST_USER,
    #         [request.user.email]
    #         )
        
    #     email.fail_silently=False
    #     email.send()
    
       
    return JsonResponse('Payment Completed', safe=False)
