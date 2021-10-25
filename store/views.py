from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

# from django.core.mail import send_mail
# from django.conf import settings

# Create your views here.

# price_1ICV7qBBFg9oIquvaWQhDmqP


def page_not_found_view(request, exception):
    return render(request, "404.html", status=404)


def home(request):
    timer = Timer.objects.all()
    context = {"timer": timer[0]}
    # return HttpResponse(" YO")
    return render(request, "store/home.html", context)


def main(request):
    timer = Timer.objects.all()
    context = {"timer": timer[0]}
    # return HttpResponse(" YO")
    return render(request, "store/main.html", context)


# def product.id(request):


def shop(request):

    data = cartData(request)
    cartItems = data["cartItems"]
    timer = Timer.objects.all()

    products = Product.objects.all()
    context = {"products": products, "cartItems": cartItems, "timer": timer[0]}
    return render(request, "store/shop.html", context)


def cart(request):
    data = cartData(request)
    print(data)
    items = data["items"]
    order = data["order"]
    cartItems = data["cartItems"]
    timer = Timer.objects.all()

    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "timer": timer[0],
    }
    return render(request, "store/cart.html", context)


def productdetails(request, id):
    data = cartData(request)
    timer = Timer.objects.all()

    cartItems = data["cartItems"]
    product = Product.objects.get(id=id)
    return render(
        request,
        "store/productId.html",
        {"product": product, "cartItems": cartItems, "timer": timer[0]},
    )


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
    items = data["items"]
    order = data["order"]
    cartItems = data["cartItems"]
    timer = Timer.objects.all()

    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "timer": timer[0],
        
    }
    # print(context)
    # print(order)

    return render(request, "store/checkout.html", context)


def updateItem(request):
    print("running")
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    stock = data["stock"]
    print("Action:", action)
    print("productId:", productId)
    print("stock", stock)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    print("qty", orderItem.quantity)
    if product.in_stock >= int(orderItem.quantity):

        if action == "add" or action == "addcart":
            orderItem.quantity = orderItem.quantity + 1
            if product.in_stock != 0:
                product.in_stock -= 1
    if action == "remove":
        product.in_stock += orderItem.quantity

        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()
    product.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse({"quantity": orderItem.quantity}, safe=False)


from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# @csrf_exempt
def processOrder(request):
    print("ok")
    data = cartData(request)
    items = data["items"]
    order = data["order"]
    cartItems = data["cartItems"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    products_list = []
    # if request.user.is_authenticated:
    #     order_cart_items = order.get_cart_items
    #     cart_total = order.get_cart_total

    #     for item in items:
    #         product_dict = {}
    #         product_dict["img"] = item.product.imageURL
    #         product_dict["name"] = item.product.name
    #         product_dict["price"] = item.product.price
    #         product_dict["quantity"] = item.quantity
    #         products_list.append(product_dict)

    # else:
    order_cart_items = order["get_cart_items"]
    cart_total = order["get_cart_total"]

    for item in items:
        product_dict = {}
        product_dict["img"] = item["product"]["imageURL"]
        product_dict["name"] = item["product"]["name"]
        product_dict["price"] = item["product"]["price"]
        product_dict["quantity"] = item["quantity"]
        products_list.append(product_dict)

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    # print('Data:', request.body)

    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)

    # else:
    customer, order = guestOrder(request, data)

    total = float(data["form"]["total"])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        shipping = ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data["shipping"]["address"],
            city=data["shipping"]["city"],
            state=data["shipping"]["state"],
            zipcode=data["shipping"]["zipcode"],
            email=data["shipping"]["email"],
        )

        product = Product.objects.filter(pk__in=data["product"])

        shipping.product.set(product)
        name = data["form"]["name"]

        email_verification(
            name,
            data["shipping"]["email"],
            data["shipping"]["address"],
            order_cart_items,
            cart_total,
            products_list,
        )

    return JsonResponse("Payment Completed", safe=False)


def email_verification(name, email1, address, cart_items, cart_total, products_list):
    subject = "Milliyar"
    message = render_to_string(
        "store/tyemail.html",
        {
            "name": name,
            "email": email1,
            "address": address,
            "cart_items": cart_items,
            "cart_total": cart_total,
            "product_list": products_list,
        },
    )
    text_context = strip_tags(message)

    email = EmailMultiAlternatives(
        subject, text_context, settings.EMAIL_HOST_USER, [email1]
    )
    email.attach_alternative(message, "text/html")
    email.send()
    print("Email succesfully sent ")
