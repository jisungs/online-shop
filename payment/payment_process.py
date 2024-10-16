from django.http import JsonResponse
from django.shortcuts import get_object_or_404

import requests
import json
from decouple import config
from iamport import Iamport



def get_token():
    access_data = {
        'imp_key':config('IAMPORT_REST_API_KEY'),
        'imp_secret':config('IAMPORT_REST_SECRET_KEY')
    }
    url = "https://api.iamport.kr/users/getToken"
    req = requests.post(url, data=access_data)
    access_res = req.json()
    if access_res['code'] == 0:
        return access_res['response']['access_token']
    else:
        return None
    

def payment_prepare(merchant_uid,  amount,*arg, **kwargs):
    access_token = get_token()
    if access_token:
        access_data = {
            'merchant_uid':merchant_uid,
            'amount': amount
        }
        json_data = json.dumps(access_data, indent=4)
        url = "https://api.iamport.kr/payments/prepare"
        headers = {
            'Content-Type':'application/json',
            'Authorization': access_token
        }
        req = requests.post(url, data = json_data, headers=headers)
        res = req.json()
        if res['code'] != 0:
            raise ValueError("API 통신 오류")
    else:
        raise ValueError("토큰 오류")
    
    



# def payment_prepare(merchant_uid, amount):
#     iamport = Iamport(
#         imp_key = config('IAMPORT_REST_API_KEY'),
#         imp_secret = config('IAMPORT_REST_SECRET_KEY')
#     )
#     merchant_uid = merchant_uid
#     amount = amount
#     try: 
#         response = iamport.prepare(
#             merchant_uid=merchant_uid,
#             amount=amount
#         )
#         print(response)
#     except Iamport.ResponseError as e:
#         return JsonResponse({'error':e.message})