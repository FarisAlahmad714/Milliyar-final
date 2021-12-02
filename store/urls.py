from django.urls import path
from django.http import HttpResponse

from . import views

urlpatterns = [
    path("", views.shop, name="shop"),
    path(
        "robots.txt/",
        lambda x: HttpResponse("User-Agent: *\nDisallow:", content_type="text/plain"),
        name="robots_file",
    ),
    path("home/", views.home, name="home"),
    path("about/", views.about, name="about"),
    # path('index/', views.index, name="index"),
    path("product/<int:id>/", views.productdetails, name="productdetails"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update_item/", views.updateItem, name="update_item"),
    path("process_order/", views.processOrder, name="process_order"),
]
