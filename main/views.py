from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from .models import Product, Profile, User

import random
import string
import stripe
import json


def create_order_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


class HomePageView(TemplateView):
    template_name = "homepage.html"


def paymentcomplete(request):
	return render(request, "payment_complete.html")


def checkout(request):
	if request.user.is_authenticated:
		cart = Profile.objects.get(user= request.user).cart
		total = cart.aggregate(Sum('product_price'))['product_price__sum']
		return render(request,"checkout.html", {"cart":cart, "total":total})
	else:
		redirect("main:homepage")


@csrf_exempt
def createpayment(request):
	if request.user.is_authenticated:
		cart  = Profile.objects.get(user=request.user).products
		# total = cart.aggregate(Sum('product_price'))['product_price__sum']
		total = 70
		total = total * 100
		stripe.api_key = settings.STRIPE_SECRET_KEY
		if request.method=="POST":
			
			data = json.loads(request.body)
			intent = stripe.PaymentIntent.create(
				customer=Profile.objects.get(user=request.user).customer_id,
				amount=total,
				currency=data['currency'],
				metadata={'integration_check': 'accept_a_payment'},
				)
			try:
				return JsonResponse({'publishableKey':	
					settings.STRIPE_PUBLISHABLE_KEY, 'clientSecret': intent.client_secret})
			except Exception as e:
				return JsonResponse({'error':str(e)},status= 403)@csrf_exempt


def paymentcomplete(request):
	if request.method=="POST":
		data = json.loads(request.POST.get("payload"))
		if data["status"] == "succeeded":
			# save purchase here/ setup email confirmation
			return render(request, "payment-complete.html")
		

def logged_in_before_check(sender, user, request, **kwargs):
	profile = User.objects.get(username=user.username) # this is the user object
	profile_obj = Profile.objects.get(user=profile) # pass object NOT STRING
	stripe.api_key = settings.STRIPE_SECRET_KEY
	if not profile_obj.logged_in_before:
		stripe.Customer.create(
			id=profile_obj.customer_id,
			email=profile_obj.user.email,
			description="Testing dynamic assignment of variables.",
		)
		Profile.objects.filter(user=profile).update(logged_in_before=True)
	else:
		print("Made it to else statement because logged in before is now True")


user_logged_in.connect(logged_in_before_check)
