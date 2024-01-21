# mtn_payment_app/mtn_integration.py
import requests
import json
from datetime import datetime
from .config import MTN_API_KEYS

class MTNIntegration:
    BASE_URL = 'https://api.mtn.com/v1'

    @staticmethod
    def get_access_token():
        token_url = f'{MTNIntegration.BASE_URL}/oauth/access_token'
        client_id = MTN_API_KEYS.get('client_id', '')
        client_secret = MTN_API_KEYS.get('client_secret', '')

        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
        }

        response = requests.post(token_url, data=data)

        if response.status_code == 200:
            return response.json().get('access_token', '')
        else:
            print(f'Failed to get access token. Status code: {response.status_code}')
            return None

    @staticmethod
    def get_headers(api_key_type='primary'):
        api_key = MTN_API_KEYS.get(api_key_type, '')
        headers = {
            'Ocp-Apim-Subscription-Key': api_key,
            'Authorization': f'Bearer {MTNIntegration.get_access_token()}'
        }
        return headers

    @staticmethod
    def create_payment(payment_data):
        url = f'{MTNIntegration.BASE_URL}/payments'
        headers = MTNIntegration.get_headers()

        payload = json.dumps(payment_data)
        headers['Content-Type'] = 'application/json'

        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Failed to create payment. Status code: {response.status_code}')
            return {'error': 'Failed to create payment'}

    @staticmethod
    def momotoken():
        url = f'{MTNIntegration.BASE_URL}/collection/token/'
        headers = {
            'Ocp-Apim-Subscription-Key': MTN_API_KEYS.get('collections_subkey', ''),
            'Authorization': f'Bearer {MTNIntegration.get_access_token()}'
        }

        response = requests.post(url, headers=headers, data={})

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Failed to get MoMo token. Status code: {response.status_code}')
            return {'error': 'Failed to get MoMo token'}

    @staticmethod
    def get_payments_by_reference(reference_id, start_date, end_date, id_type='MSISDN', page_number=1, page_size=10, status=None):
        url = f'{MTNIntegration.BASE_URL}/payments/reference/{reference_id}'
        headers = MTNIntegration.get_headers('collections_subkey')

        params = {
            'idType': id_type,
            'startDate': start_date,
            'endDate': end_date,
            'pageNumber': page_number,
            'pageSize': page_size,
            'status': status,
            # Include other parameters as needed
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Failed to get payment history. Status code: {response.status_code}')
            return {'error': 'Failed to get payment history'}

# Usage example:
reference_id = 'your_reference_id'
start_date = '2024-01-01'
end_date = '2024-12-31'
payment_history = MTNIntegration.get_payments_by_reference(reference_id, start_date, end_date)

print(payment_history)
