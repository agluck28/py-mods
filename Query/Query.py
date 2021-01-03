'''
Creates a query instance that will be used to help build
up queries to extract data from an influxDB instance
'''

class Query():
    '''
    Creates a Query instance that will operate off if a given bucket
    The filter will be built up to look for a query that matches all tags
    When providing the fields input, that will be built as an Or statemtn
    In order to utilize the function, pass Query.query into an
    influxdb client query instance
    '''

    def __init__(self, bucket):
        '''
        Initializes a query object. This query object will always have the same bucket. Methods will be provided
        to update the time range and filters used.
        '''
        self.bucket = bucket
        #initialize query base with the not changing part, tags and fields can be updated
        self.query = f'from(bucket: "{self.bucket}")' 
        #f'|> range(start: {self.range[0]}{self.range[1]})'
        #f'|> filter(fn: (r) => r._measurement == "{self.measurement}"')

    def add_measurement_filter(self, measurement):
        self.query = self.query + f'|> filter(fn: (r) => r._measurement == "{measurement}")'

    def add_time_range(self, time_range=(-1,'h')):
        self.query = self.query + f'|> range(start: {time_range[0]}{time_range[1]})'

    def add_field_filter(self, *fields):
        '''
        Generates a filter for fields. These will be by or if multiple are specified as each field is unique
        '''
        filters = []
        for field in fields:
            filters.append(f'r._field == "{field}"')
            #add or filter keyword
            filters.append('or')
        #remove last element, was added for ease of coding. Then convert to string and add to query
        filters.pop()
        self.__add_filter(filters)

    def add_tag_filter(self, tags_dict, filterType='and'):
        '''
        Adds tags filters that must all be present. The tags argument passed in should be a dictonary of tag names
        as the key and the values as the value. Filter type can be either and or or. This will specify if all tags must be found
        or if just one. The deault is and
        '''
        filters = []
        for key, value in tags_dict.items():
            filters.append(f'r.{key} == "{value}"')
            filters.append(filterType)
        
        filters.pop()
        self.__add_filter(filters)

    def __add_filter(self, filters):
        '''
        Intended to be a private function that is called everytime tags or fields are added
        '''
        #string with filter up to measurement already present set querybase to query so it can be built up
        self.query = self.query + '|> filter(fn: (r) => ' + ' '.join(map(str, filters)) + ')'

if __name__ == "__main__":
    bucket = 'home'
    time_range = (-1, 'h')
    measurement = 'home'
    fields = ['humidity', 'temperature']

    test_query = Query(bucket)
    test_query.add_time_range(time_range)
    test_query.add_measurement_filter(measurement)
    test_query.add_field_filter('humidity', 'temperature')
    test_query.add_tag_filter({'tag1': 'value1', 'tag2': 'value3'}, 'or')
    print(test_query.query)

