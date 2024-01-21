from django.urls import path
from .views import *

app_name = 'mtn_payment_app'

urlpatterns = [
    path('make-payment/', make_payment, name='make_payment'),
]
