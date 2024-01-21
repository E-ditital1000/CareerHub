from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from .forms import *
from .models import *
from django.http import JsonResponse
from .mtn_integration import MTNIntegration
from .forms import PaymentForm
from django.contrib import messages


def make_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_data = form.cleaned_data
            response = MTNIntegration.create_payment(payment_data)
            return JsonResponse(response)
        else:
            print(form.errors)
    else:
        form = PaymentForm()

    return render(request, 'mtn_payment_app/make_payment.html', {'form': form})


