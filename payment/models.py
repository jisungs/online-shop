from django.db import models
from orders.models import Order
from .payment_process import payment_prepare

import hashlib
# Create your models here.

class PaymentTransactionManager(models.Manager):
    def create_new(self,order,amount, success=None, trasaction_status=None):
        if not order:
            raise ValueError("주문오류")
        
        order_hash = hashlib.sha1(str(order.id).encode('utf-8')).hexdigest()
        email_hash = "upgradeafterloginmodules"
        final_hash = hashlib.sha1((order_hash  + email_hash).encode('utf-8')).hexdigest()[:10]        
        merchant_order_id = "%s"%(final_hash)

        # payment_prepare(merchant_order_id= merchant_order_id, amount=amount)

        transaction = self.model(
            order = order,
            merchant_order_id=merchant_order_id,
            amount = amount
        )

        if success != None:
            transaction.success = success
            transaction.transaction_status = trasaction_status
        
        try:
            transaction.save()
        except Exception as e:
            print("save error", e)

        return transaction.merchant_order_id

class PaymentTransaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    merchant_order_id = models.CharField(max_length=120, null=True, blank=True)
    transaction_id = models.CharField(max_length=120, null=True, blank=True)
    amount = models.PositiveIntegerField(default=0)
    transaction_status = models.CharField(max_length=220, null=True, blank=True)
    type = models.DateTimeField(auto_now_add=True, auto_now=False)
    created = models.DateTimeField(auto_now_add=True,auto_now=False)

    objects = PaymentTransactionManager()

    def __str__(self):
        return str(self.order.id)
    
    class Meta:
        ordering = ['-created']