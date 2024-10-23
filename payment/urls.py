from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('vaildataion/', views.payment_validation, name='validation'),

    path('completed/', views.payment_completed, name='completed'),
    path('failded/', views.payment_failed, name='failed'),

    path('canceled/', views.payment_canceled, name='canceled'),
]