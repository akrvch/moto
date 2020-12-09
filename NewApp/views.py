from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm, NonLoggedOrderForm


# view домашней страницы


def home_view(request):
    return render(request, 'home.html')


# view страницы магазина


def shop_view(request):
    bikes = Motorcycle.objects.all()
    moto_types = MotoTypes.objects.all()
    vendors = MotoVendor.objects.all()
    return render(request, 'shop.html', {'bike_list': bikes, 'moto_types': moto_types, 'vendors': vendors})


# view поиска


def search(request):
    moto_types = MotoTypes.objects.all()
    vendors = MotoVendor.objects.all()
    s = request.GET.get('search')
    bikes = Motorcycle.objects.filter(Q(brand__vendor__contains=s) | Q(moto_model__contains=s))
    return render(request, 'shop.html', {'bike_list': bikes, 'moto_types': moto_types, 'vendors': vendors})


# view добавления в корзину


def add_to_cart(request, pk, page):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if request.user.is_authenticated:
        item = Motorcycle.objects.get(pk=pk)
        cart, create = Cart.objects.get_or_create(user=request.user, item=item)
        cart.count = int(cart.count) + 1
        cart.save()

    else:
        if x_forwarded_for:
            user = x_forwarded_for.split(',')[0]
            item = Motorcycle.objects.get(pk=pk)
            cart, create = NonLoggedCart.objects.get_or_create(user=user, item=item)
            cart.count = int(cart.count) + 1
            cart.save()
        else:
            user = request.META.get('REMOTE_ADDR')
            item = Motorcycle.objects.get(pk=pk)
            cart, create = NonLoggedCart.objects.get_or_create(user=user, item=item)
            cart.count = int(cart.count) + 1
            cart.save()
    return redirect(page)


# view страницы корзины


def detail_cart(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    """Опередляем залогинен ли юзер"""
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(Q(user=request.user))
    else:
        if x_forwarded_for:
            user = x_forwarded_for.split(',')[0]
            cart_items = NonLoggedCart.objects.filter(Q(user=user))
        else:
            user = request.META.get('REMOTE_ADDR')
            cart_items = NonLoggedCart.objects.filter(Q(user=user))
    pks = [item.get('item_id') for item in cart_items.values()]             # pks - получаем список pk товаров в корзине
    total = 0                                                               # total - общая цена всех товаров в корзине
    """Проходимся циклом по всем мотоциклам с pk из pks"""
    for pk in pks:
        bike = Motorcycle.objects.filter(Q(pk=pk))                          # bike - объект товара
        cart_bike = cart_items.filter(Q(item_id=pk))                        # cart_bike - товар из корзины для получения количества
        count = [i['count'] for i in cart_bike.values()]                    # count - получение списка с количеством товара
        price = [i['price'] for i in bike.values()]                         # price - получение списка с ценой товара
        total += count[0] * price[0]
    item_count = [i['count'] for i in cart_items.values()]                  #item_count - общее количество товаров в корзине
    return render(request, 'cart.html', {'items': cart_items, 'summary': sum(item_count), 'total': total})


# view Очистки корзины


def clear_cart(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(Q(user=request.user))
        cart_items.delete()
    else:
        if x_forwarded_for:
            user = x_forwarded_for.split(',')[0]
            cart_items = NonLoggedCart.objects.filter(Q(user=user))
            cart_items.delete()
        else:
            user = request.META.get('REMOTE_ADDR')
            cart_items = NonLoggedCart.objects.filter(Q(user=user))
            cart_items.delete()
    return redirect('cart')


# view для удаления конкретного товара из корзины


def delete_item(request, pk):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(Q(user=request.user))
    else:
        if x_forwarded_for:
            user = x_forwarded_for.split(',')[0]
            cart_items = NonLoggedCart.objects.filter(Q(user=user))
        else:
            user = request.META.get('REMOTE_ADDR')
            cart_items = NonLoggedCart.objects.filter(Q(user=user))
    item = cart_items.filter(pk=pk)
    item.delete()
    return redirect('cart')


# view для фильтров


def shop_filter(request):
    moto_types = MotoTypes.objects.all()
    vendors = MotoVendor.objects.all()
    req = request.GET
    try:
        if len(req) == 3:
            bikes = Motorcycle.objects.filter(Q(brand__vendor__in=request.GET.getlist('vendor')),
                                              Q(type__id__in=request.GET.getlist('type')),
                                              Q(newbie__in=request.GET.getlist('newbie')))

        elif len(req) == 2:
            if 'vendor' in req and 'type' in req:
                bikes = Motorcycle.objects.filter(Q(brand__vendor__in=request.GET.getlist('vendor')),
                                                  Q(type__id__in=request.GET.getlist('type')))

            elif 'vendor' in req and 'newbie' in req:
                bikes = Motorcycle.objects.filter(Q(brand__vendor__in=request.GET.getlist('vendor')),
                                                  Q(newbie__in=request.GET.getlist('newbie')))

            else:
                bikes = Motorcycle.objects.filter(Q(type__id__in=request.GET.getlist('type')),
                                                  Q(newbie__in=request.GET.getlist('newbie')))

        elif len(req) == 1:
            bikes = Motorcycle.objects.filter(Q(brand__vendor__in=request.GET.getlist('vendor')) |
                                              Q(type__id__in=request.GET.getlist('type')) |
                                              Q(newbie__in=request.GET.getlist('newbie')))

        else:
            bikes = Motorcycle.objects.all()
    except ValueError:
        return redirect('shop')
    return render(request, 'shop.html', {'bike_list': bikes, 'moto_types': moto_types, 'vendors': vendors})


# view с формой оформления заказа


def order(request):
    if request.user.is_authenticated:
        form = OrderForm(request.GET or None)
    else:
        form = NonLoggedOrderForm(request.GET or None)
    return render(request, 'order.html', {'form': form})


# view для привязки товаров к нужному заказу


def new_order(request, *args, **kwargs):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if request.user.is_authenticated:
        form = OrderForm(request.GET or None)
        user = request.user
    else:
        if x_forwarded_for:
            user = x_forwarded_for.split(',')[0]
        else:
            user = request.META.get('REMOTE_ADDR')
        form = NonLoggedOrderForm(request.GET or None)
        """Заполняем модель данными полученными из формы"""
    if form.is_valid():
        order = form.save(commit=False)
        order.user = user
        order.name = form.cleaned_data['name']
        order.surname = form.cleaned_data['surname']
        order.email = form.cleaned_data['email']
        order.tele_num = form.cleaned_data['tele_num']
        order.delivery = form.cleaned_data['delivery']
        order.save()

        if request.user.is_authenticated:
            user = request.user
            cart = Cart.objects.filter(user=user)
            count_id = -1
            """ Задаем нужно количество итераций для цикла в зависимости от того, сколько товаров в списке """
            for n in range(len(cart.values('item'))):
                """ Получаем нужные айтемы и их количество из крозины """
                pk_list = [i['item'] for i in cart.values('item')]
                count = [i['count'] for i in cart.values('count')]
                bike = Motorcycle.objects.get(pk=int(pk_list[n]))
                order_pk = (len(Order.objects.filter(user=user))) - 1           # order_pk - индекс послденего заказа юзера
                order = Order.objects.filter(user=user).order_by('pk')[order_pk]
                count_id += 1
                """ Создаем айтем, связанный с нужным нам заказом """
                ordered_item, create = OrderItem.objects.get_or_create(item=bike, count=count[count_id], order_id=order, user=user)
                clean_cart = Cart.objects.filter(user=user)                     # clean_cart - находим корзину для очистки
                ordered_item.save()
                order_items = OrderItem.objects.filter(order_id=order)
        else:
            if x_forwarded_for:
                user = x_forwarded_for.split(',')[0]
            else:
                user = request.META.get('REMOTE_ADDR')
            cart = NonLoggedCart.objects.filter(user=user)
            count_id = -1
            for n in range(len(cart.values('item'))):
                pk_list = [i['item'] for i in cart.values('item')]
                count = [i['count'] for i in cart.values('count')]
                bike = Motorcycle.objects.get(pk=int(pk_list[n]))
                order_pk = (len(NonLoggedOrder.objects.filter(user=user))) - 1
                order = NonLoggedOrder.objects.filter(user=user).order_by('pk')[order_pk]
                count_id += 1
                ordered_item, create = NonLoggedOrderItem.objects.get_or_create(item=bike, count=count[count_id],
                                                                                order_id=order)
                clean_cart = NonLoggedCart.objects.filter(user=user)
                ordered_item.save()
                order_items = NonLoggedOrderItem.objects.filter(order_id=order)
    """ Очищаем корзину """
    clean_cart.delete()
    return render(request, 'order.html', {'order': order, 'items': order_items})


# view страницы котнтактной инфы


def contacts(request):
    return render(request, 'contacts.html')


# view страницы инфы по гарантии


def guarantee(request):
    return render(request, 'guarantee.html')


# view страницы инфы по доставке


def delivery(request):
    return render(request, 'delivery.html')


# view страницы инфы по оплате


def oplata(request):
    return render(request, 'oplata.html')


# view страницы детального обзора товара


def shop_detailed(request, pk):
    item = Motorcycle.objects.filter(pk=pk)
    return render(request, 'details.html', {'items': item})


# view страницы с историе заказов пользователя


def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    order_items = OrderItem.objects.filter(user=request.user)
    print(orders, order_items)
    return render(request, 'my_orders.html', {'orders': orders, 'items': order_items})