from django.urls import path
from .views import HomePageView

from . import views

app_name = 'main'

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('checkout', views.checkout, name='checkout'),
    path("create-payment-intent", views.createpayment, name="create-payment-intent"),
    path("payment-complete", views.paymentcomplete, name="payment-complete"),

]