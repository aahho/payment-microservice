from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField
from stripe_service.managers.PaymentRequestManager import PaymentRequestManager
import datetime

class PaymentRequest(models.Model):
    id = models.AutoField(primary_key=True)
    pass_key = models.CharField(max_length=255)
    amount = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    geo_location = JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(default=datetime.datetime.now()+datetime.timedelta(minutes=3))

    request_manager = PaymentRequestManager()

    class Meta:
        db_table = 'payment_request'
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        new = super(PaymentRequest, self).save(*args, **kwargs)
        return self