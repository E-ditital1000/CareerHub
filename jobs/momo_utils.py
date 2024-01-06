import requests
from django.conf import settings

def create_api_user(reference_id, callback_host):
    url = "https://sandbox.momodeveloper.mtn.com/collection/token/apiuser"
    headers = {
        "Authorization": f"Bearer {settings.MOMO_API_PRIMARY_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "providerCallbackHost": callback_host,
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def create_api_key(api_user_id):
    url = f"https://sandbox.momodeveloper.mtn.com/collection/token/apiuser/{api_user_id}/apikey"
    headers = {
        "Authorization": f"Bearer {settings.MOMO_API_PRIMARY_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers)
    return response.json()

def get_api_user_details(api_user_id):
    url = f"https://sandbox.momodeveloper.mtn.com/collection/token/apiuser/{api_user_id}"
    headers = {
        "Authorization": f"Bearer {settings.MOMO_API_PRIMARY_KEY}",
    }
    response = requests.get(url, headers=headers)
    return response.json()
