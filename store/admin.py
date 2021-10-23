from django.contrib import admin
from django.utils.html import format_html
from django.db import models

# Register your models here.
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

# Register your models here.

from .models import *
from django.contrib.admin.widgets import AdminFileWidget


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(
                u' <a href="%s" target="_blank"><img src="%s" alt="%s" width="150" height="150"  style="object-fit: cover;"/></a> %s '
                % (image_url, image_url, file_name, _(""))
            )
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return format_html(u"".join(output))


class ProductImage(admin.TabularInline):
    model = ProductImages
    formfield_overrides = {models.ImageField: {"widget": AdminImageWidget}}


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImage]
    formfield_overrides = {models.ImageField: {"widget": AdminImageWidget}}

    def image_tag(self, obj):
        try:
            return format_html('<img width=100 src="{}" />'.format(obj.image.url))
        except:
            return None

    image_tag.short_description = "Image"

    list_display = ["image_tag", "name", "price"]


class ShippingAddressAdmin(admin.StackedInline):
    model = ShippingAddress


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem


admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
# admin.site.register(ProductColor)
class OrderADmin(admin.ModelAdmin):
    inlines = [ShippingAddressAdmin, OrderItemAdmin]
    list_display = ("date_ordered", "customer", "id")


admin.site.register(Order, OrderADmin)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(ProductImages)
admin.site.register(Timer)
