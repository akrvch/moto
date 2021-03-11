from django.contrib import admin
from .models import Motorcycle, MotoVendor, MotoTypes, Cart, NonLoggedCart, Order, OrderItem


class MotoAdminPanel(admin.ModelAdmin):
    list_display = ['brand', 'type', 'engine', 'price', 'max_speed', 'power', 'date_release', 'date_adding']


admin.site.register(Motorcycle, MotoAdminPanel)
admin.site.register(MotoVendor)
admin.site.register(MotoTypes)
admin.site.register(Cart)
admin.site.register(NonLoggedCart)
admin.site.register(Order)
admin.site.register(OrderItem)
