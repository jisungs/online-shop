from django.urls import path
from . import views

urlpatterns = [
    path('payment/',views.payment_request, name='payment_request'),
    path('pay/check/<str:merchant_uid>/', views.check_payment, name='check_payment'),
    path('pay/verify/<int:product_price>/<str:merchant_uid>/', views.verify_payment, name='verify_payment'),
    path('pay/cancel/<str:merchant_uid>/', views.cancel_payment, name='cancel_payment'),
]