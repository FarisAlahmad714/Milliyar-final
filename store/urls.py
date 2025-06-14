from django.urls import path
from django.http import HttpResponse


from . import views

urlpatterns = [
    path("", views.shop, name="shop"),
    path("home/", views.home, name="home"),
    path("newhome/", views.newhome, name="newhome"),
    path("about/", views.about, name="about"),
    path("product/<int:id>/", views.productdetails, name="productdetails"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update_item/", views.updateItem, name="update_item"),
    path("process_order/", views.processOrder, name="process_order"),
    path('create-checkout-session/', views.CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
    path('health/', views.health_check, name='health_check'),
]