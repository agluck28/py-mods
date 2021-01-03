import pymongo, sys
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
        rooms = {}
        for room in self.rooms.find():
            objId = str(room['_id'])
            rooms[objId] = room['name']
        return rooms

    def get_room_info(self, roomId):
        '''
        returns information about a given room. Requires passing in the room Id
        return data will be the name or the room and an array of deviceIds of what 
        devices are in the room
        '''
        #define filter
        f = Connection.create_filter(self, roomId)
        roomObj = self.rooms.find_one(f)
        devices = []
        for device in roomObj['devices']:
            devices.append(str(device))
        room = {
            'name': roomObj['name'],
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
        devices = {}
        for device in self.devices.find():
            objId = str(device['_id'])
            devices[objId] = device['name']
        return devices

    def get_device_info(self, deviceId):
        '''
        Returns information about the device. Information returned will be the roomId it is located in,
        the types of measurements it supports, the type of device it is and the rate at which it measures
        the given measurements
        '''
        f = Connection.create_filter(self, deviceId)
        deviceObj = self.devices.find_one(f)
        device = {
            'name': deviceObj['name'],
            'type': deviceObj['type'],
            'type_info': deviceObj['type_info'],
            'roomId': str(deviceObj['roomId'])
        }
        return device