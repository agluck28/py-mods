import requests
import json

'''
Handles the connection to th smartthings server API for v1
Will return responses in dictonaries
Assumes an Oauth2 token has already been obtains, does not have support
for obtaining or generating one yourself
'''

# SmartThings is cloud based, URL is the same for all users
api_url = 'https://api.smartthings.com/v1/'


class StConnection():
    '''
    Connection handler for a smart things API version, handles sending the needed
    requested to the cloud and will abstract away needing to know about GET, POST or PUT
    Requires having an already existing bearer token
    '''

    def __init__(self, token):
        '''
        Generates needed header and sets URL
        '''
        self._url = api_url
        self.header = {'Authorization': f'Bearer {token}'}

    def send_GET(self, endpoint):
        return requests.get(self._url + endpoint, headers=self.header)

    def send_POST(self, endpoint, data):
        return requests.post(self._url + endpoint, data=data, headers=self.header)


def list_locations(StConnection):
    '''
    Returns a dictonary of locations with key the id and value the name
    '''
    response = StConnection.send_GET('/locations')
    if response.status_code == 200:
        locations = {}
        for location in json.loads(response.text)['items']:
            locations[location['locationId']] = location['name']
        return locations
    else:
        # if not a successful response, return the code and text
        return f'Getting Locations failed with response code {response.status_code}\n {response.text}'


def list_rooms(StConnection, locationId):
    '''
    Returns all rooms from a given location
    Return will be a dictonary of roomIds as keys and the name as the value
    '''
    response = StConnection.send_GET(f'/locations/{locationId}/rooms')
    if response.status_code == 200:
        rooms = {}
        for room in json.loads(response.text)['items']:
            rooms[room['roomId']] = room['name']
        return rooms
    else:
        return f'Getting Rooms failed with response code {response.status_code}\n {response.text}'


def list_devices(StConnection):
    '''
    Will return all devices for the given smartthings account
    return will be a dictonary of deviceId as the key and label as the value
    '''
    response = StConnection.send_GET('/devices')
    if response.status_code == 200:
        devices = {}
        for device in json.loads(response.text)['items']:
            try:
                new_device = {}
                new_device['roomId'] = device['roomId']
            except KeyError:
                new_device['roomId'] = 'None'
            finally:
                new_device['name'] = device['label']
                new_device['type'] = device['type']
                devices[device['deviceId']] = new_device
        return devices
    else:
        return f'Getting devices failed with response code {response.status_code}\n {response.text}'

def get_device_status(StConnection, deviceId):
    '''
    Will return the status information about the device
    This will return the full device status components object from smartthings
    Device specific decorators will be needed to handle return types for various needs
    '''
    response = StConnection.send_GET(f'/devices/{deviceId}/status')
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return f'Getting device status failed with response code {response.status_code}\n {response.text}'


if __name__ == "__main__":
    pass