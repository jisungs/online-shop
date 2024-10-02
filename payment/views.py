from django.shortcuts import render, get_object_or_404,redirect
from django.conf import settings
from django.urls import reverse
from orders.models import Order


def payment_process(request):
    return render(request, 'payment/process.html')
