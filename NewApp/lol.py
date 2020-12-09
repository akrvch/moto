if request.user.is_authenticated:
    user = request.user
    cart = Cart.objects.filter(user=user)
    for n in range(len(cart.values('item'))):
        items = [i['item'] for i in cart.values('item')]
        count = [i['count'] for i in cart.values('count')]
        or_id = (len(Order.objects.filter(user=user))) - 1
        form = OrderItemForm()
        order_item = form.save(commit=False)
        order_item.order_id = or_id
        order_item.item = items[n]
        order_item.count = count[n]
        order_item.save()
else:
    if x_forwarded_for:
        user = x_forwarded_for.split(',')[0]
    else:
        user = request.META.get('REMOTE_ADDR')
    cart = NonLoggedCart.objects.filter(user=user)
    for n in range(len(cart.values('item'))):
        items = [i['item'] for i in cart.values('item')]
        count = [i['count'] for i in cart.values('count')]
        or_id = (len(NonLoggedOrder.objects.filter(user=user))) - 1
        form = NonLoggedOrderItemForm()
        order_item = form.save(commit=False)
        order_item.order_id = or_id
        order_item.item = items[n]
        order_item.count = count[n]
        order_item.save()
