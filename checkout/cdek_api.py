import requests
from django.core.cache import cache


class CdekApi:
    URL = 'https://api.edu.cdek.ru/v2/'
    ACCOUNT = 'wqGwiQx0gg8mLtiEKsUinjVSICCjtTEP'
    SECRET = 'RmAmgvSgSl1yirlz9QupbzOJVqhCxcP5'

    def _get_token(self):
        token = cache.get('cdek_token')
        if token:
            return token
        response = requests.post(
            self.URL + 'oauth/token',
            data={
                'grant_type': 'client_credentials',
                'client_id': self.ACCOUNT,
                'client_secret': self.SECRET,
            },
            headers={'Accept': 'application/json'},
        )
        response.raise_for_status()
        data = response.json()
        cache.set('cdek_token', data['access_token'], data['expires_in'] - 60)
        return data['access_token']

    def search_cities(self, query):
        token = self._get_token()
        response = requests.get(
            self.URL + 'location/cities',
            params={'city': query, 'size': 10},
            headers={'Authorization': f'Bearer {token}'},
        )
        response.raise_for_status()
        return response.json()

    def get_pvz(self, city_code=None):
        token = self._get_token()
        params = {}
        if city_code:
            params['city_code'] = city_code
        response = requests.get(
            self.URL + 'deliverypoints',
            params=params,
            headers={'Authorization': f'Bearer {token}'},
        )
        response.raise_for_status()
        return response.json()
