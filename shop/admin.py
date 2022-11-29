from django.contrib import admin

from shop.models import Product, Payment, Order, OrderItem

admin.site.register(Product)
admin.site.register(Payment)
admin.site.register(OrderItem)
admin.site.register(Order)
