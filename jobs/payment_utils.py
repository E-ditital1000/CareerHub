
import requests
import json

def create_api_user(api_user_id, subscription_key, reference_id, callback_host):
    base_url = "https://sandbox.momodeveloper.mtn.com"
    endpoint = "/apiuser"
    
    headers = {
        "X-Reference-Id": reference_id,
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/json",
    }

    data = {
        "providerCallbackHost": callback_host,
    }

    response = requests.post(f"{base_url}{endpoint}", headers=headers, json=data)

    return response.json()

def create_api_key(api_user_id, subscription_key):
    base_url = "https://sandbox.momodeveloper.mtn.com"
    endpoint = f"/apiuser/{api_user_id}/apikey"

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/json",
    }

    response = requests.post(f"{base_url}{endpoint}", headers=headers)

    return response.json()

def get_api_user_details(api_user_id, subscription_key):
    base_url = "https://sandbox.momodeveloper.mtn.com"
    endpoint = f"/apiuser/{api_user_id}"

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
    }

    response = requests.get(f"{base_url}{endpoint}", headers=headers)

    return response.json()

