from django.http import JsonResponse
from django.shortcuts import render

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import stripe

from api.models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(['GET'])
def get_checkout_session(request, id):
    item = get_object_or_404(Item, id=id)
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": item.stripe_price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url='http://localhost:8000/success/',
        cancel_url='http://localhost:8000/cancel/',
    )
    return JsonResponse({"session_id": checkout_session.id})


@api_view(['GET'])
def get_item_page(request, id):
    item = get_object_or_404(Item, id=id)
    return render(request, 'item_detail.html', {'item': item, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})


@api_view(['POST'])
def test_payment(request):
    test_payment_intent = stripe.PaymentIntent.create(
        amount=1000, currency='pln',
        payment_method_types=['card'],
        receipt_email='test@example.com')
    return Response(status=status.HTTP_200_OK, data=test_payment_intent)


def success(request):
    return render(request, 'success.html')


def cancel(request):
    return render(request, 'cancel.html')
