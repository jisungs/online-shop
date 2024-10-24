from django.shortcuts import render, get_object_or_404,redirect
from django.conf import settings
from django.urls import reverse
from orders.models import Order
from .models import *

from decouple import config
from iamport import Iamport
from django.http import JsonResponse

from .payment_process import get_token

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    shop_id = config('IAMPORT_SHOP_KEY')
    price = 0

    item_name = ""
    for item in order.items.all():
        item_name = item.product.name
        price = int(item.price)
   
    merchant_id = PaymentTransaction.objects.create_new(
        order=order,
        amount =price
    )

    context = {
        "order_id" : order_id,
        "shop_id" : shop_id,
        "merchant_id":merchant_id,
        "item_name":item_name,
        "amount":price
    }
    return render(request, 'payment/process.html', context)


def payment_validation(request):
    print('검증 함수 실행')
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        merchant_id = request.POST.get('merchant_id')
        # merchant_id = PaymentTransaction.objects.get(order=order)
        imp_id = request.POST.get('imp_id')
        amount = request.POST.get('amount')
        print(f'port 안 데이터 {order_id}\n,{merchant_id}\n,{amount}\n,{order}\n')
        try:
            trans = PaymentTransaction.objects.get(
                order = order,
                merchant_order_id = merchant_id,
                amount = amount
            )
        except Exception as e:
            trans = None
        print(f'만들어진 주문데이터{trans}')
        if trans != None:
            trans.transaction_id = imp_id
            trans.success=True
            trans.save()
            order.paid =True
            order.save()

            data = {
                "works":True
            }
            print(f'처리후 데이터 {data}')
            return JsonResponse(data)
        else:
            return JsonResponse({}, status = 401)


def payment_completed(request):
    order_id = request.GET.get('order_id')
    order = Order.objects.get(id=order_id)
    return render(request, 'payment/complete.html', {'order':order})


def payment_failed(request):
    return render(request, 'payment/failed.html')

def payment_request(request):
    iamport = Iamport(
        imp_key = config('IAMPORT_API_KEY'),
        imp_secret = config('IAMPORT_REST_SECRET_KEY')
    )

    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
     
    merchant_uid = 'order_id_12345'
    amount = 100 

    try: 
        response = iamport.prepare(
            merchant_uid=merchant_uid,
            amount=amount
        )
    except Iamport.ResponseError as e:
        return JsonResponse({'error':e.message})
    

def check_payment(request, merchant_uid):
    iamport = Iamport(
        imp_key = config('IAMPORT_API_KEY'),
        imp_secret = config('IAMPORT_REST_SECRET_KEY')
    )

    #상품 아이디로 결재 정보 확인
    try:
        response =iamport.find(merchant_uid=merchant_uid)
        return JsonResponse(response)
    except Iamport.ResponseError as e:
        return JsonResponse({'error':e.error})
    

def verify_payment(request, product_price, merchant_uid):
    iamport = Iamport(
        imp_key = config('IAMPORT_API_KEY'),
        imp_secret = config('IAMPORT_REST_SECRET_KEY')
    )

    try:
        is_paid=iamport.is_paid(product_price, merchant_uid=merchant_uid)
        if is_paid:
            return JsonResponse({'message': 'Payment verified successfully'})
        else:
            return JsonResponse({'message':'payment verification failed'})
    except Iamport.ResponseError as e:
        return JsonResponse({'error':e.message})
    

def payment_canceled(request, merchant_uid):
    iamport = Iamport(
        imp_key = config('IAMPORT_API_KEY'),
        imp_secret = config('IAMPORT_REST_SECRET_KEY'))

    try:
       response = iamport.cancel('취소사유', merchant_uid=merchant_uid)
       return JsonResponse(response)
    except Iamport.ResponseError as e:
       return JsonResponse({'error':e.message})
    



