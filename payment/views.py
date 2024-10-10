from django.shortcuts import render, get_object_or_404,redirect
from django.conf import settings
from django.urls import reverse
from orders.models import Order

from decouple import config
from iamport import Iamport
from django.http import JsonResponse


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    print(f'주문번호는 : {order_id}')
    for item in order.items.all():
        print(item.price)
        print(item.product.name)
        print(item.quantity)

    
    context = {
        "order_id" : order_id, 
    }
    return render(request, 'payment/process.html', context)

def payment_completed(request):
    return render(request, 'payment/complete.html')

def payment_request(request):
    iamport = Iamport(
        imp_key = config('IAMPORT_API_KEY'),
        imp_secret = config('IAMPORT_REST_SECRET_KEY')
    )

    merchant_uid = 'order_id_12345'
    amount = 100 #결재금액

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
    

