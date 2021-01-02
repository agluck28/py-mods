import base64
import requests
import json


class AuthHw():
    '''
    Handles the oauth2 for Honeywell Thermostats
    Assumes the code has already been obtained via the webpage
    Requires passing in the code, api key and secret. Will provide the ability
    to obtain the bearer token used for oauth2 with Honeywell, and also a method
    to refresh to token
    '''

    def __init__(self, apikey, secret, code):
        '''
        Initializes the base connection string along with base64 encoding
        of the apikey and secret to be utilized with Basic Auth to obtain the
        bearer token
        '''
        self._url = 'https://api.honeywell.com/oauth2/'
        self.apikey = apikey
        # generate and set header for basic auth
        msg = apikey + ':' + secret
        base64_basic = self._get_base64(msg)
        self.headers = {
            'Authorization': f'Basic {base64_basic}'
        }
        self.code = code
        self.accessToken = ''
        self.bearer = {
            'token': '',
            'expire': 0
        }
        self.refreshToken = ''
        self.oauth2_header = {}

    def _get_base64(self, data):
        return base64.b64encode(data.encode('ascii')).decode('ascii')

    def get_access_token(self):
        '''
        Gets the access token that will need to be fed to obtain
        authorization code/bearer token used
        '''
        data = {
            'grant_type': 'client_credentials'
        }
        response = requests.post(url=self._url+'accesstoken', headers=self.headers, data=data)
        # check for successful response
        if response.status_code == 200:
            self.accessToken = json.loads(response.text)['access_token']
            return self.accessToken
        else:
            return f'Unable to get access token.\nResponse Code: {response.status_code}\nMessage: {response.text}'

    def get_oauth2(self):
        '''
        Retrieves the needed bearer token and refresh token, also sets the
        expiration for the bearer token
        '''
        temp_header = self.headers.copy()
        temp_header['Accept'] = 'application/json'
        data = {
            'grant_type': 'authorization_code',
            'code': self.code,
            'redirect_uri': 'none'
        }

        response = requests.post(url=self._url+'/token', headers=self.headers, data=data)
        if response.status_code == 200:
            dict_data = json.loads(response.text)
            self.bearer['token'] = dict_data['access_token']
            self.bearer['expire'] = dict_data['expires_in']
            self.refreshToken = dict_data['refresh_token']
            self.set_oauth2_header()
        else:
            return f'Request failed.\nResponse Code: {response.status_code}\nMessage: {response.text}'

    def refresh_token(self):
        '''
        refreshes the bearer token and updates the expiration and the token
        '''
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refreshToken
        }

        response = requests.post(url=self._url+'/token', headers=self.headers, data=data)
        if response.status_code == 200:
            dict_data = json.loads(response.text)
            print(dict_data)
            self.bearer['token'] = dict_data['access_token']
            self.bearer['expire'] = dict_data['expires_in']
            self.refreshToken = dict_data['refresh_token']
            self.set_oauth2_header()
        else:
            return f'Request failed.\nResponse Code: {response.status_code}\nMessage: {response.text}'

    def set_oauth2_header(self):
        '''
        returns a header dictonary with the bearer token set that can be passed into
        the requests library
        '''
        self.oauth2_header = {'Authorization': f"Bearer {self.bearer['token']}"}


if __name__ == "__main__":
    pass