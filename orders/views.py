from django.urls import reverse
from django.shortcuts import render, redirect

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem
from .tasks import order_created

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order = order,
                    product = item['product'],
                    price = item['price'],
                    quantity = item['quantity']
                )
            cart.clear()
            #비동기 작업으로 주문이 생성되면 메일을 전송
            # order_created.delay(order.id)
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))
            # return render(request, 'orders/order/created.html', {'order':order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart':cart, 'form':form})
