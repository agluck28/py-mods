import pymongo
import sys
from bson import ObjectId


class Connection():
    '''
    Parent class just used to handle opening and closing the connection, since
    it is the same for both rooms and devices
    '''

    def __init__(self, dburl, database):
        '''
        opens the connection to the given database
        '''
        self.client = pymongo.MongoClient(dburl)

    def close(self):
        self.client.close()

    def create_filter(self, objId):
        '''
        simple internal function used to map the id to an Object id for a filter to pass to 
        a find() function
        '''
        f = {
            '_id': ObjectId(objId)
        }
        return f


class Rooms(Connection):
    '''
    Opens a connection to the rooms collection in the database
    It will be responsible for returning the list of rooms within the database and also 
    for returning more detailed info about a given room. Eventually support will be added for 
    creating and updating rooms
    '''

    def __init__(self, dburl, database):
        '''
        opens the connection to the given database and sets the rooms object,
        after verifying it exists. This is to assist with querying later on
        dburl assumes username and password are included
        '''
        Connection.__init__(self, dburl, database)
        self.rooms = self.client[database].rooms

    def get_rooms(self):
        # initialize empty rooms list that will build up the retrieved info
        rooms = []

        # this retrieves all rooms in the rooms collections
        for room in self.rooms.find():

            # create empty device list to hold IDs of the returned devices
            devices = []
            for device in room['devices']:
                tempDevice = {
                    'id': str(device)
                }
                devices.append(tempDevice)
            # build up room items to return to caller
            tempRoom = {
                'id': str(room['_id']),
                'room_name': room['name'],
                'devices': devices
            }
            rooms.append(tempRoom)
        return rooms

    def get_room_info(self, roomId):
        '''
        returns information about a given room. Requires passing in the room Id
        return data will be the name or the room and an array of deviceIds of what 
        devices are in the room
        '''
        # define filter
        f = Connection.create_filter(self, roomId)
        roomObj = self.rooms.find_one(f)
        devices = []
        for device in roomObj['devices']:
            tempDevice = {
                'id': str(device)
            }
            devices.append(tempDevice)
        room = {
            'id': roomId,
            'room_name': roomObj['name'],
            'devices': devices
        }
        return room


class Devices(Connection):
    '''
    Opens a connection to the devices collection in the passed in database.
    This will support retriving all devices along with info about given devices. Eventually support will
    be added to add new devices
    '''

    def __init__(self, dburl, database):
        Connection.__init__(self, dburl, database)
        self.devices = self.client[database].devices

    def get_devices(self):
        devices = []
        for device in self.devices.find():
            devices.append((str(device['_id']), self._form_device(device)))
        return devices

    def get_device_info(self, deviceId):
        '''
        Returns information about the device. Information returned will be the roomId it is located in,
        the types of measurements it supports, the type of device it is and the rate at which it measures
        the given measurements
        '''
        f = Connection.create_filter(self, deviceId)
        deviceObj = self.devices.find_one(f)
        return (str(deviceObj['_id']), self._form_device(deviceObj))

    def get_device_measurements(self, deviceId):
        '''
        Returns the current measurements of the device
        '''
        devId, device = self.get_device_info(deviceId)
        return device['measurements']

    def set_device_measurement(self, deviceId, measurement):
        '''
        Updates the specified measurement for the provided deviceId
        measurement is a python dictonary of the values to update
        '''
        f = Connection.create_filter(self, deviceId)
        for Key, Value in measurement.items():
            update = {'$set': {f"measurements.{Key}": Value}}
            self.devices.update_one(f, update)

    def _form_device(self, deviceObj):
        return {
            'name': deviceObj['name'],
            'type': deviceObj['type'],
            'measurements': deviceObj['measurements'],
            'roomId': str(deviceObj['roomId'])
        }
