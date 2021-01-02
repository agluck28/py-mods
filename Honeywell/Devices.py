from Honeywell.auth_hw import AuthHw
import requests
import json

class Lyric():
    '''
    Creates a connection to a given Lyric thermostat that will allow the retrieval
    of the current mode, the indoor and outdoor temperatures and the indoor humidity.
    Will also return the current cooling setpoint and the heating setpoint. Also provides
    ability to set the temperature or change the mode. Assumes a single location and a single
    thermostat in that location
    '''
    def __init__(self, AuthHw, base_url='https://api.honeywell.com/v2/'):
        '''
        AuthHw is an already initialized object that contains the needed bearer token information
        A method is also provided that can be used to refresh the token through the Lyric class
        '''
        self.auth = AuthHw
        self._url = base_url
        self.location = {}
        self.device = {}
    
    def set_location_and_device_id(self):
        '''
        Assuming only a single location and a single device, this will send a request
        to get the locations, and then take the first locationID and the first device in the devices
        array from that location as the devices locationID and deviceID. This is to help with getting
        device info and setting device info in other functions
        '''
        url = self._url + 'locations'
        params = {
            'apikey': self.auth.apikey
        }
        response = requests.get(url=url, headers=self.auth.oauth2_header, params=params)
        if response.status_code == 200:
            #sets a data dictonary of the lication id and name with the devices for the location included.
            #devices include only the deviceID and name
            locations = json.loads(response.text)
            self.location = {
                'id': locations[0]['locationID'],
                'name': locations[0]['name']
                }
            self.device = {
                'id': locations[0]['devices'][0]['deviceID'],
                'name': locations[0]['devices'][0]['name']
            }
        else:
            return f'Unable to complete request.\nStatus Code: {response.status_code}\nMessage: {response.text}'

    def get_thermostat_info(self):
        '''
        This must be called after set_location_and_device_id. This will retrieve the device info
        '''
        params = {
            'apikey': self.auth.apikey,
            'locationId': self.location['id']
        }

        response = requests.get(url=self._url + f"devices/thermostats/{self.device['id']}", headers=self.auth.oauth2_header, params=params)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return {
                'status_code': response.status_code,
                'message': response.text 
            }

if __name__ == "__main__":
    pass