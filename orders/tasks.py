from celery import shared_task
from django.core.mail import send_mail

from .models import Order


@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = (
        f'{order.first_name} 고객님,\n\n'
        f'주문이 정상적으로 완료되었습니다. 상품을 준비 중입니다.'
        f'고객님의 주문 번호는 {order.id} 입니다.'
    )
    mail_sent = send_mail(
        subject, message, 'admin@myshop.com', [order.email]
    )
    print('메일이 정상적으로 전송되었습니다.')
    return mail_sent