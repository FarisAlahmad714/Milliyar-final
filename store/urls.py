from django.urls import path
<<<<<<< HEAD
from django.http import HttpResponse
=======
>>>>>>> ac87dae9c259870ce7ad63b7918d93d9a34248b2

from . import views

urlpatterns = [
    path("", views.shop, name="shop"),
<<<<<<< HEAD
    path(
        "robots.txt/",
        lambda x: HttpResponse("User-Agent: *\nDisallow:", content_type="text/plain"),
        name="robots_file",
    ),
    path("home/", views.home, name="home"),
    path("about/", views.about, name="about"),
=======
    path("home/", views.home, name="home"),
    path('about/', views.about, name="about"),
>>>>>>> ac87dae9c259870ce7ad63b7918d93d9a34248b2
    # path('index/', views.index, name="index"),
    path("product/<int:id>/", views.productdetails, name="productdetails"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update_item/", views.updateItem, name="update_item"),
    path("process_order/", views.processOrder, name="process_order"),
]
