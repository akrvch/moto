from django.contrib.auth import get_user_model
from django.db import models

# Модель производителя


class MotoVendor(models.Model):
    vendor = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.vendor


# Модель типов мотоциклов


class MotoTypes(models.Model):
    type = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Тип мотоцикла'
        verbose_name_plural = 'Типы мотоциклов'

    def __str__(self):
        return self.type


# Модель мотоцикла


class Motorcycle(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to='moto/')
    moto_model = models.CharField(max_length=50)
    brand = models.ForeignKey(MotoVendor, max_length=30, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    type = models.ForeignKey(MotoTypes, max_length=30, on_delete=models.CASCADE)
    engine = models.CharField(max_length=50)
    max_speed = models.IntegerField()
    power = models.IntegerField()
    description = models.TextField(max_length=1000)
    date_release = models.DateField(auto_now=False)
    date_adding = models.DateTimeField(auto_now_add=True)
    newbie = models.BooleanField(default=False)
    weight = models.IntegerField(default=0)
    public = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Мотоцикл'
        verbose_name_plural = 'Мотоциклы'

    def __str__(self):
        return f'{self.brand} {self.moto_model}'


# Модель корзины для незарегистрированного пользователя


class NonLoggedCart(models.Model):
    user = models.CharField(null=True, blank=True, max_length=30)
    item = models.ForeignKey(Motorcycle, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)


# Модель корзины для зарегистрированного пользователя


class Cart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    item = models.ForeignKey(Motorcycle, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)


# Модель заказа зарегистрированного пользователя


class Order(models.Model):
    ODESSA = 'Odessa'
    KIEV = 'Kiev'
    DNEPR = 'Dnepr'
    DELIVERY_TYPES = (
        (ODESSA, 'Одесса'),
        (KIEV, 'Киев'),
        (DNEPR, 'Днепр'),
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=30, verbose_name='Имя')
    surname = models.CharField(max_length=30, verbose_name='Фамилия')
    email = models.EmailField(blank=True, null=True)
    tele_num = models.IntegerField(default=380)
    delivery = models.CharField(max_length=100,
                                choices=DELIVERY_TYPES,
                                default=KIEV)

    def __str__(self):
        return str(self.id)


# Модель заказа незарегистрированного пользователя


class NonLoggedOrder(models.Model):
    ODESSA = 'Odessa'
    KIEV = 'Kiev'
    DNEPR = 'Dnepr'
    DELIVERY_TYPES = (
        (ODESSA, 'Одесса'),
        (KIEV, 'Киев'),
        (DNEPR, 'Днепр'),
    )
    user = models.CharField(null=True, blank=True, max_length=30)
    name = models.CharField(max_length=30, verbose_name='Имя')
    surname = models.CharField(max_length=30, verbose_name='Фамилия')
    email = models.EmailField(blank=True, null=True)
    tele_num = models.IntegerField(default=380)
    delivery = models.CharField(max_length=100,
                                choices=DELIVERY_TYPES,
                                default=KIEV)


# Модель заказанного товара незарегистрированного пользователя


class NonLoggedOrderItem(models.Model):
    order_id = models.ForeignKey(NonLoggedOrder, on_delete=models.CASCADE)
    item = models.ForeignKey(Motorcycle, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)


# Модель заказанного товара зарегистрированного пользователя


class OrderItem(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=1)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Motorcycle, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
