from __future__ import unicode_literals
from stripe_service.queyset.CustomersQuerySet import CustomersQuerySet
from django.db import models

class CustomersManager(models.Manager):

	def get_queryset(self):
		return CustomersQuerySet(self.model, using=self._db)

	def get_active_customers(self):
		return self.get_queryset().get_active_customers()

	def get_by_keys(self, filterBy):
		return self.get_queryset().get_by_keys(filterBy)

	def fetch_defered_by_keys(self, filterBy, selectFields):
		return self.get_queryset().fetch_defered_by_keys(filterBy, selectFields)

	def get_banned_customers(self):
		return self.get_queryset().get_banned_customers()

	def get_deleted_users(self):
		return self.get_queryset().get_deleted_users()