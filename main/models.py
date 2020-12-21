from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver 
from django.db.models.signals import post_save

import random
import string


class Product(models.Model):
	product_name = models.CharField(max_length=150, blank=True, null=True)
	product_type = models.CharField(max_length=25, blank=True, null=True)
	product_description = models.TextField(blank=True, null=True)
	product_price = models.IntegerField(blank=True, null=True)




class Profile(models.Model):  
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	cart = models.ManyToManyField(Product, related_name='cart_test')
	logged_in_before = models.BooleanField(default=False)
	customer_id = models.CharField(default='cus_'+
	''.join(random.choices(string.ascii_lowercase + string.digits, k=20)), max_length=24)

	@receiver(post_save, sender=User) 
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User) 
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()