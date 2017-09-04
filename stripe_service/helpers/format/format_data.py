from payment_service import helper
import json

def store_customer(customer):
	new = {
		'id' : str(helper.generate_uuid()),
		'email' : customer.email,
		'customer_id' : customer.id,
		'currency' : customer.currency,
		'description' : customer.description,
		'is_livemode' : customer.livemode,
		'extras' : customer
	}
	return new