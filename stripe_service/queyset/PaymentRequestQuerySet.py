from django.db import models
import datetime

class PaymentRequestQuerySet(models.QuerySet):

	## 
	# Filter
	# return querySet
	##
	def get_by_keys(self, filterBy):
		return self.filter(**filterBy)

	def validate(self, pass_key):
		return self.filter(pass_key=pass_key, expires_at__gte=datetime.datetime.now())

	def expire_token(self, pass_key):
		return self.filter(pass_key=pass_key).update(**{'expires_at':datetime.datetime.now()})