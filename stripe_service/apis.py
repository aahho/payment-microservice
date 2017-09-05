import stripe, json, datetime
from stripe_service.helpers.format import format_data
from stripe_service.models.Customers import Customers
from stripe_service.models.PaymentRequest import PaymentRequest
from payment_service import helper
from ast import literal_eval
from payment_service import Controller

stripe.api_key = "sk_test_OzUxP5dwzancBE1GIomJ8qjw"
stripe.api_base = "https://api.stripe.com"
stripe.api_version = '2017-08-15'

def handle(func_name, request):
	stripe_api = StripeApis(func_name, request)
	return stripe_api.get()

class StripeApis():

	def __init__(self, func_name, request = {}):
		self.func_name = func_name
		self.request = request

	def get(self):
		def func_not_found():
			return Controller.respondWithError(404, 'We messed up!', 'Function not defined')
		try:
			return getattr(self, self.func_name, func_not_found)(self.request)
		except stripe.error.CardError as e:
			body = e.json_body
  			err  = body.get('error', {})
			return Controller.respondWithError(e.http_status, err.get('message'), 'Error From Api. Card Error!')
		except stripe.error.InvalidRequestError as e:
			body = e.json_body
  			err  = body.get('error', {})
			return Controller.respondWithError(e.http_status, err.get('message'), 'Error From Api. Invalid Request Error!')
		except stripe.error.AuthenticationError as e:
			body = e.json_body
  			err  = body.get('error', {})
			return Controller.respondWithError(e.http_status, err.get('message'), 'Error From Api. Authentication Error!')
		except stripe.error.APIConnectionError as e:
			body = e.json_body
  			err  = body.get('error', {})
			return Controller.respondWithError(e.http_status, err.get('message'), 'Error From Ap. Connection Error!')
		except stripe.error.StripeError as e:
			body = e.json_body
  			err  = body.get('error', {})
			return Controller.respondWithError(e.http_status, err.get('message'), 'Error From Api. Api Error!')
		except Exception as e:
			return Controller.respondWithError(500, 'We messed up!', 'Something Went Wrong')

	def fetch_customer(self, request):
		payment_details = PaymentRequest.request_manager.validate(request.GET['secure_key'])
		if len(payment_details):
			customer = Customers.customer_manager.get_by_keys({'email':payment_details[0].email})
			card_meta = []
			if len(customer):
				cards = customer[0].extras['sources']['data']
				for card in cards:
					new = {
						'id' : card['id'],
						'email' : customer[0].email,
						'customer_name' : card['name'],
						'card_brand' : card['brand'],
						'digits' : card['last4'],
						'exp_year' : card['exp_year'],
						'exp_month' : card['exp_month'],
						'zip_code' : card['address_zip']
					}
					card_meta.append(new)
			details = {
				'amount' : payment_details[0].amount,
				'email' : payment_details[0].email,
				'location' : literal_eval(payment_details[0].geo_location) if payment_details[0].geo_location != None else {},
				'cards' : card_meta
			}
			return details
		return Controller.respondWithError(401, 'Unauthorised Request', 'Invalid secure key request')

	def initialize(self, request):
		data = {
			'pass_key' : str(helper.generate_pass_key()),
			'email' : request.POST.get('email'),
			'amount' : request.POST.get('amount'),
			'geo_location' : helper.get_location(request),
			'expires_at' : datetime.datetime.now()+datetime.timedelta(minutes=5)
		}
		new_request = PaymentRequest(**data).save()
		customer = Customers.customer_manager.get_by_keys({'email':data['email']})
		card_meta = []
		if len(customer):
			cards = customer[0].extras['sources']['data']
			for card in cards:
				new = {
					'customer_name' : card['name'],
					'card_brand' : card['brand'],
					'digits' : card['last4'],
					'exp_year' : card['exp_year'],
					'exp_month' : card['exp_month'],
					'zip_code' : card['address_zip']
				}
				card_meta.append(new)
		if new_request:
			data['cards'] = card_meta
			return data
		return Controller.respondWithError(500, 'We messed up!', 'Failed to generate request')

	def find_or_create_customer(self, request, token):
		customer = Customers.customer_manager.get_by_keys({'email':token.email})
		if len(customer):
			if 'secure_save' in request.POST and request.POST.get('secure_save') == 'on':
				customer_details = stripe.Customer.retrieve(customer[0].customer_id).sources.create(card=request.POST.get('stripeToken', ''))
				customer_afterupdate = stripe.Customer.retrieve(customer[0].customer_id)
				
				## VALIDATING AND DELETING CARDS
				card_fingerprints = []
				for card in customer_afterupdate['sources']['data']:
					if card.fingerprint not in card_fingerprints:
						card_fingerprints.append(card.fingerprint)
					else:
						customer_afterupdate.sources.retrieve(card.id).delete()
				
				## UPDATING LOCAL DATABASE WITH CUSTOMER NEW CARD DATA
				customer[0].extras = stripe.Customer.retrieve(customer[0].customer_id)
				customer[0].save()
			return customer[0]
		else:
			customer = stripe.Customer.create(
				card = request.POST.get('stripeToken', ''),
	            email = token.email
			)
			new = format_data.store_customer(customer)
			customer = Customers(**new).save()
			return customer

	def create_payment(self, request):
		if 'secure_key' in request.GET:
			token = PaymentRequest.request_manager.validate(request.GET['secure_key'])
			if len(token):
				if 'is_fromsaved' in request.GET and request.GET['is_fromsaved'] == 'True':
					customer = Customers.customer_manager.get_by_keys({'email':request.POST.get('email')})
					if not len(customer):
						return Controller.respondWithError(500, 'Transaction Failed', 'Invalid Customer')
					cards = customer[0].extras['sources']['data']
					is_card_valid = False
					for card in cards:
						if request.POST.get('id') == card['id']:
							is_card_valid = True
					if not is_card_valid:
						return Controller.respondWithError(500, 'Transaction Failed', 'Invalid Card Provided')
					charge = stripe.Charge.create(
						amount = token[0].amount,
						currency = 'INR',
						customer = str(customer[0].customer_id),
						card = str(request.POST.get('id')),
						idempotency_key = str(helper.generate_uuid())
					)
				else:
					customer = self.find_or_create_customer(request, token[0])
					charge = stripe.Charge.create(
						amount = token[0].amount,
						currency = "INR",
						customer = customer.customer_id,
						description = "Charge for "+customer.email,
						idempotency_key = str(helper.generate_uuid()),
						metadata = {
							'display_name' : request.POST['cardholder-name'],
							'phone_number' : request.POST['phone-number']
						}
					)
				if charge:
					PaymentRequest.request_manager.expire_token(request.GET['secure_key'])
					return Controller.respondWithSuccess(201, 'Payment Transaction Successful')
				return Controller.respondWithError(500, 'Transaction Failed', 'Please try again')
			else:
				return Controller.respondWithError(400, 'Invalid Token Provided', 'Please try again')
		return Controller.respondWithError(400, 'Bad Request', 'Request token not found')
