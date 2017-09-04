from stripe_service import apis
from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from payment_service import Controller
from helpers.format import format_data

def start(request):
	return render(request, "demo_input.html")

def initiate_payment(request):
	if request.method == 'GET':
		return Controller.respondWithError(405, 'Request Method Not Allowed', 'Try other secure method')
	data = apis.handle('initialize', request)
	if data['pass_key'] is not None:
		return redirect('/payment/charge?secure_key='+data['pass_key'])
	return data

def create_payment(request):
	if request.method == 'GET':
		pass_key = request.GET['secure_key']
		data = apis.handle('fetch_customer', request)
		if 'email' in  data:
			return render(request, 'index.html', {'pass_key':pass_key, 'data':data})
		return data

	return apis.handle('create_payment', request)
