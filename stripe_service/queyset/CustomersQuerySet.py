from django.db import models

class CustomersQuerySet(models.QuerySet):

	## 
	# Fetch all active customers
	# return querySet
	##
	def get_active_customers(self):
		filterBy = {
			'deleted_at': None,
			'is_active' : True,
			'is_banned' : False
		}
		return self.filter(**filterBy)

	## 
	# Fetch all active customers
	# return querySet
	##
	def get_by_keys(self, filterBy):
		filterBy.update({'deleted_at':None})
		return self.filter(**filterBy)

	## 
	# Select Fields
	# return querySet
	##
	def fetch_defered_by_keys(self, filterBy, selectFields):
		filterBy.update({'deleted_at':None})
		return self.filter(**filterBy).defer(*selectFields)

	## 
	# Fetch all banned customers
	# return querySet
	##
	def fetch_banned(self):
		filterBy = {
			'deleted_at': None,
			'is_banned' : True,
		}
		return self.filter(**filterBy)

	## 
	# Fetch all deleted customers
	# return querySet
	##
	def fetch_deleted(self):
		return self.filter(deleted_at_isnull=False)

	## 
	# Update User
	# Ban/Unban status
	# return bool
	##
	def update(self, filterBy, updateBy):
		return self.filter(**filterBy).update(**updateBy)

	## 
	# Delete user by id
	# return bool
	##
	def delete(self, filterBy):
		return self.filter(**filterBy).delete()