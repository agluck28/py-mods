from influxdb_client import Point, WritePrecision

class PointWriter():
    '''
    Creates a class that will help with writes to an influxDB
    This will define the Point by having it setup with fields that
    do not change after creation, measurement and tags. The fields
    will be left off, along with the time, and will be added in the create_line call
    '''

    def __init__(self, measurement, *tags):
        '''
        Initializies the PointWriter. Will setup the point with the tags passed in which
        will be a list of tuples. Measurement is a string
        '''
        #initalize point with measurement name
        self._Point = Point(measurement)
        #check that tuples are passed in as the tags
        for tag in tags:
            if type(tag) != tuple:
                raise TypeError('Tags must be passed in as tuples')
            else:
                self._Point = self._Point.tag(tag[0], tag[1])


    def add_fields(self, fieldset, time):
        '''
        Adds the fields along with the value. Time is also added
        in this call. The return is a Point object that can be used
        to write to the DB. Fieldset is a dictonary of key value pairs
        '''
        #check if fieldset is a dict
        if type(fieldset) != dict:
            raise TypeError('fieldset must be passed as a dict')
        else:
            #place added fields in new temporary variable
            #this allows self._Point to be reused
            tempPoint = None
            for key, value in fieldset.items():
                tempPoint = self._Point.field(key, value)
            return tempPoint.time(time, WritePrecision.NS)

if __name__ == "__main__":
    NewPoint = PointWriter('test1',("tag1","value1"),("tag2","value2"))
    print(NewPoint._Point._tags)



        