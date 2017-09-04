from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField
from stripe_service.managers.CustomersManager import CustomersManager

class Customers(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    email = models.CharField(max_length=100)
    customer_id = models.CharField(max_length=100)
    currency = models.CharField(max_length=20, null=True)
    description = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False)
    is_livemode = models.BooleanField()
    extras = JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    customer_manager = CustomersManager()

    class Meta:
        db_table = 'customers'
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        new = super(Customers, self).save(*args, **kwargs)
        return self