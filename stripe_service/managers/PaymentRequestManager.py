from __future__ import unicode_literals
from stripe_service.queyset.PaymentRequestQuerySet import PaymentRequestQuerySet
from django.db import models

class PaymentRequestManager(models.Manager):

	def get_queryset(self):
		return PaymentRequestQuerySet(self.model, using=self._db)

	def get_by_keys(self, filter_by):
		return self.get_queryset().get_by_keys(filter_by)

	def validate(self, pass_key):
		return self.get_queryset().validate(pass_key)

	def expire_token(self, pass_key):
		return self.get_queryset().expire_token(pass_key)