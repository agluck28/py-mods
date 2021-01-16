from Query.Query import Query
from Flux.Flux import parse_table

'''
Helps to build up queries to an influx DB instance and to parse the resulting
response. 
'''

class HelperQuery():
    '''
    simple class to be used for holding the base query that is used for all
    '''

    def __init__(self, bucket, roomId, time_range):
        self.room_data = Query(bucket)
        self.room_data.add_time_range(time_range)
        self.room_data.add_measurement_filter(roomId)

def get_all_room_data(bucket, roomId, time_range=(-30,'m')):
    '''
    returns a query that can be used to retreive all device
    measurements for a given room for a given time range
    '''

    return HelperQuery(bucket, roomId, time_range).room_data.query

def get_single_room_data(bucket, roomId, device, time_range=(-30, 'm')):
    '''
    returns a query that can be used to retrieve data about a single sensor
    '''
    device_query = HelperQuery(bucket, roomId, time_range)
    device_query.room_data.add_field_filter(device)

    return device_query.room_data.query


if __name__ == "__main__":
    print(get_all_room_data('home', '123123'))
    print(get_single_room_data('home', '321', 'thisdevice'))