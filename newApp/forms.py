from django.forms import ModelForm
from .models import *


# Форма оформления заказа для зарегистрированного пользователя

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['user']


# Форма оформления заказа для зарегистрированного пользователя


class NonLoggedOrderForm(ModelForm):
    class Meta:
        model = NonLoggedOrder
        fields = '__all__'
        exclude = ['user']
