# import stripe
from django.core.mail import EmailMessage
from django.views import View
from django.shortcuts import redirect
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
import logging
from django.db import transaction
from django.db.models import F
from django.views.decorators.cache import cache_page
from django.core.cache import cache
# from django_ratelimit.decorators import ratelimit
# from django_ratelimit.exceptions import Ratelimited

# stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)

# from django.core.mail import send_mail
# from django.conf import settings

# Create your views here.

# price_1ICV7qBBFg9oIquvaWQhDmqP


def page_not_found_view(request, exception):
    return render(request, "404.html", status=404)

def health_check(request):
    """Simple health check endpoint for Vercel"""
    from django.http import JsonResponse
    return JsonResponse({"status": "ok", "message": "Django is running on Vercel"})


@cache_page(60 * 15)  # Cache for 15 minutes
def home(request):
    timer = Timer.objects.all()
    context = {"timer": timer[0]}
    # return HttpResponse(" YO")
    return render(request, "store/home.html", context)


def newhome(request):
    timer = Timer.objects.all()
    context = {"timer": timer[0]}
    # return HttpResponse(" YO")
    return render(request, "store/newhome.html", context)


def main(request):
    timer = Timer.objects.all()
    context = {"timer": timer[0]}
    return render(request, "store/main.html", context)


def about(request):
    timer = Timer.objects.all()
    context = {
        "timer": timer[0],
        "object": {
            "title": "About",
            "slug": "about",
            "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsu",
        },
    }

    # slug
    # description- content
    # title
    return render(request, "store/about.html", context)


# def index(request):
#     return render(request, "store/index.html")


@cache_page(60 * 15)  # Cache for 15 minutes
def shop(request):

    data = cartData(request)
    cartItems = data["cartItems"]
    timer = Timer.objects.all()

    products = Product.objects.all()
    context = {
        "products": products,
        "cartItems": cartItems,
        "timer": timer[0],
        "object": {
            "title": "Shop",
            "slug": "shop",
            "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsu",
        },
    }
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
        "object": {
            "title": "Cart",
            "slug": "cart",
            "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsu",
        },
    }
    return render(request, "store/cart.html", context)


def productdetails(request, id):
    data = cartData(request)
    timer = Timer.objects.all()

    cartItems = data["cartItems"]
    product = Product.objects.get(id=id)
    return render(
        request,
        "store/productID.html",
        {
            "product": product,
            "cartItems": cartItems,
            "timer": timer[0],
            "object": {
                "title": product.name,
                "slug": f"product/{product.id}",
                "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsu",
            },
        },
    )


# stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_success(request):
    return render(request, 'store/success.html')

def payment_cancel(request):
    return render(request, 'store/cancel.html')



# @ratelimit(key='ip', rate='10/m', method='POST')  # 10 checkout attempts per minute per IP
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = cartData(request)
            items = data["items"]
            order_data = data["order"]
            
            # Check if using mock payments or real Stripe
            if settings.USE_MOCK_PAYMENTS:
                # Mock checkout - processes order without payment gateway
                # Use atomic transaction to prevent race conditions
                try:
                    with transaction.atomic():
                        # Check and decrease stock atomically
                        for item in items:
                            product = Product.objects.select_for_update().get(id=item['product']['id'])
                            if product.in_stock >= item['quantity']:
                                product.in_stock = F('in_stock') - item['quantity']
                                product.save(update_fields=['in_stock'])
                            else:
                                return JsonResponse({
                                    "error": f"Insufficient stock for {item['product']['name']}. Only {product.in_stock} available."
                                }, status=400)
                        
                        if request.user.is_authenticated:
                            # Get or create customer for authenticated user
                            customer, created = Customer.objects.get_or_create(
                                user=request.user,
                                defaults={'name': request.user.username, 'email': request.user.email}
                            )
                            # Get or create the actual order object
                            order, created = Order.objects.get_or_create(
                                customer=customer, 
                                complete=False
                            )
                            order.complete = True
                            order.save()
                            
                            # Send order confirmation email
                            try:
                                send_order_confirmation_email(customer.name, customer.email, order, items)
                            except Exception as email_error:
                                logger.error(f"Email error: {email_error}")
                        else:
                            # Handle guest checkout - create temporary order for processing
                            logger.info("Guest checkout completed")
                            
                except Exception as e:
                    logger.error(f"Order processing error: {e}")
                    return JsonResponse({"error": "Order processing failed. Please try again."}, status=500)
                
                # Clear cart and redirect to success
                response = JsonResponse({
                    'redirect_url': request.build_absolute_uri('/success/')
                })
                response.delete_cookie('cart')
                return response
            
            else:
                # Real Stripe checkout (uncomment when ready)
                # import stripe
                # stripe.api_key = settings.STRIPE_SECRET_KEY
                
                # product_data = json.loads(request.body)
                # checkout_session = stripe.checkout.Session.create(
                #     payment_method_types=['card'],
                #     line_items=[{
                #         'price_data': {
                #             'currency': 'usd',
                #             'product_data': {
                #                 'name': item['product']['name'],
                #             },
                #             'unit_amount': int(item['product']['price'] * 100),
                #         },
                #         'quantity': item['quantity'],
                #     } for item in items],
                #     mode='payment',
                #     success_url=request.build_absolute_uri('/success/'),
                #     cancel_url=request.build_absolute_uri('/cancel/'),
                # )
                # return JsonResponse({'sessionId': checkout_session.id})
                
                return JsonResponse({"error": "Real payments not configured yet"}, status=400)
                
        except Exception as e:
            print(f"Error processing order: {e}")
            return JsonResponse({"error": "An error occurred"}, status=500)

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
        "stripe_publishable_key": settings.STRIPE_PUBLIC_KEY,  # Add this line
        "object": {
            "title": "Checkout",
            "slug": "checkout",
            "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsu",
        },
    }
    # print(context)
    # print(order)

    return render(request, "store/checkout.html", context)


# @ratelimit(key='ip', rate='60/m', method='POST')  # 60 requests per minute per IP
def updateItem(request):
    try:
        logger.info(f"UpdateItem request - User: {request.user}, Body: {request.body}")
        data = json.loads(request.body)
        productId = int(data["productId"])
        action = data["action"]
        
        if request.user.is_authenticated:
            logger.info(f"Authenticated user cart update - Product: {productId}, Action: {action}")
            # Authenticated user - use database cart
            with transaction.atomic():
                # Get or create customer for authenticated user
                customer, created = Customer.objects.get_or_create(
                    user=request.user,
                    defaults={'name': request.user.username, 'email': request.user.email}
                )
                logger.info(f"Customer: {customer.name}, Created: {created}")
                
                # Use select_for_update to prevent race conditions
                product = Product.objects.select_for_update().get(id=productId)
                logger.info(f"Product: {product.name}, Stock: {product.in_stock}")
                
                order, created = Order.objects.get_or_create(
                    customer=customer, complete=False)
                logger.info(f"Order: {order.id}, Created: {created}")
                
                orderItem, created = OrderItem.objects.get_or_create(
                    order=order, product=product)
                logger.info(f"OrderItem: {orderItem.id}, Quantity: {orderItem.quantity}, Created: {created}")

                # Only update cart quantities, don't modify stock until checkout
                if action == "add" or action == "addcart":
                    # Check if adding this item would exceed available stock
                    if orderItem.quantity < product.in_stock:
                        orderItem.quantity = F('quantity') + 1
                        orderItem.save(update_fields=['quantity'])
                        # Refresh to get actual value
                        orderItem.refresh_from_db()
                        logger.info(f"Item added, new quantity: {orderItem.quantity}")
                    else:
                        logger.warning(f"Not enough stock - requested: {orderItem.quantity + 1}, available: {product.in_stock}")
                        return JsonResponse({"error": "Not enough stock available"}, status=400)
                        
                elif action == "remove":
                    if orderItem.quantity > 1:
                        orderItem.quantity = F('quantity') - 1
                        orderItem.save(update_fields=['quantity'])
                        orderItem.refresh_from_db()
                        logger.info(f"Item removed, new quantity: {orderItem.quantity}")
                    else:
                        orderItem.delete()
                        logger.info("Item deleted from cart")
                        return JsonResponse({"quantity": 0}, safe=False)

                return JsonResponse({"quantity": orderItem.quantity}, safe=False)
        else:
            # Anonymous user - use cookie cart (existing behavior)
            product = Product.objects.get(id=productId)
            logger.info(f"Anonymous user cart update - Product: {product.name}")
            return JsonResponse({"message": f"{product.name} was updated"}, safe=False)
        
    except Exception as e:
        logger.error(f"UpdateItem error: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return JsonResponse({"error": f"Unable to update cart: {str(e)}"}, status=500)


# @csrf_exempt

# @ratelimit(key='ip', rate='5/m', method='POST')  # 5 order submissions per minute per IP
def processOrder(request):
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
        address = data["shipping"]["address"]
        city = data["shipping"]["city"]
        state = data["shipping"]["state"]

        email_verification(
            name,
            data["shipping"]["email"],
            address,
            city,
            state,
            order_cart_items,
            cart_total,
            products_list,
        )

    return JsonResponse("Payment Completed", safe=False)


def email_verification(
    name, email1, address, city, state, cart_items, cart_total, products_list
):
    subject = "Milliyar"
    message = render_to_string(
        "store/tyemail.html",
        {
            "name": name,
            "email": email1,
            "address": address,
            "city": city,
            "state": state,
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


def send_order_confirmation_email(name, email_address, order, items):
    """Send order confirmation email to customer"""
    try:
        subject = "Order Confirmation - Milliyar"
        
        # Calculate totals
        cart_total = sum(item['get_total'] for item in items)
        cart_items = sum(item['quantity'] for item in items)
        
        # Prepare product list for email
        products_list = []
        for item in items:
            product_dict = {
                "img": item["product"]["imageURL"],
                "name": item["product"]["name"], 
                "price": item["product"]["price"],
                "quantity": item["quantity"],
                "total": item["get_total"]
            }
            products_list.append(product_dict)
        
        message = render_to_string(
            "store/tyemail.html",
            {
                "name": name,
                "email": email_address,
                "cart_items": cart_items,
                "cart_total": cart_total,
                "product_list": products_list,
                "order_id": order.id,
                "order_date": order.date_ordered
            },
        )
        text_context = strip_tags(message)

        email = EmailMultiAlternatives(
            subject, text_context, settings.EMAIL_HOST_USER, [email_address]
        )
        email.attach_alternative(message, "text/html")
        email.send()
        print(f"Order confirmation email sent to {email_address}")
        
    except Exception as e:
        print(f"Failed to send order confirmation email: {e}")
        raise e
