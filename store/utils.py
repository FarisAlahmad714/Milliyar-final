import json
from .models import *


def guestOrder(request, data):
    print("User Not Logged In")

    print("COOKIES:", request.COOKIES)
    name = data["form"]["name"]
    email = data["form"]["email"]

    cookieData = cookieCart(request)
    items = cookieData["items"]

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
        product = Product.objects.get(id=item["product"]["id"])

        orderItem = OrderItem.objects.create(
            product=product, order=order, quantity=item["quantity"]
        )
        product.in_stock -= item["quantity"]
        product.save()

    return customer, order


def cartData(request):
    if request.user.is_authenticated:
        # Authenticated user - use database cart
        try:
            customer = Customer.objects.get(user=request.user)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
            
            # Convert to the format expected by templates
            formatted_items = []
            for item in items:
                formatted_items.append({
                    'product': {
                        'id': item.product.id,
                        'name': item.product.name,
                        'price': item.product.price,
                        'imageURL': item.product.imageURL,
                    },
                    'quantity': item.quantity,
                    'get_total': item.get_total,
                    'in_stock': item.product.in_stock
                })
            
            return {"cartItems": cartItems, "order": order, "items": formatted_items}
        except Customer.DoesNotExist:
            # Customer doesn't exist yet, return empty cart
            return {"cartItems": 0, "order": {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}, "items": []}
    else:
        # Anonymous user - use cookie cart
        cookieData = cookieCart(request)
        items = cookieData["items"]
        order = cookieData["order"]
        cartItems = cookieData["cartItems"]
        return {"cartItems": cartItems, "order": order, "items": items}


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES["cart"])
    except:
        cart = {}

    print("Cart:", cart)
    items = []
    order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
    cartItems = order["get_cart_items"]

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = product.price * cart[i]["quantity"]

            order["get_cart_total"] += total
            order["get_cart_items"] += cart[i]["quantity"]

            item = {
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "imageURL": product.imageURL,
                },
                "quantity": cart[i]["quantity"],
                "get_total": total,
                "in_stock":product.in_stock
            }
            items.append(item)

            if product.digital == False:
                order["shipping"] = True

        except:
            pass

    return {"cartItems": cartItems, "order": order, "items": items}
