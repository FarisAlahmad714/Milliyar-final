from django.urls import path

from . import views

urlpatterns = [
    path('', views.shop, name="shop"),
    path('home/', views.home, name="home"),
    # path('about/', views.about, name="about"),
    path('product/<int:id>/',views.productdetails , name="productdetails"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    ]
