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

    def __init__(self, bucket, time_range, measurement, tags=[], fields=[]):
        self.bucket = bucket
        self.measurement = measurement
        self.range = time_range
        self.tags = list(tags)
        self.query = ''
        self.fields = list(fields)
        #initialize query base with the not changing part, tags and fields can be updated
        self._querybase = (f'from(bucket: "{self.bucket}")' 
        f'|> range(start: {self.range}h)'
        f'|> filter(fn: (r) => r._measurement == "{self.measurement}"')

        #initalize any passed in tags and fields
        self.__update_query()

    def add_tags_filter(self, *tags):
        for tag in tags:
            self.tags.append(tag)
        self.__update_query()

    def add_fields_filter(self, *fields):
        for field in fields:
            self.fields.append(field)
        self.__update_query()

    def __update_query(self):
        '''
        Intended to be a private function that is called everytime tags or fields are added
        '''
        #string with filter up to measurement already present set querybase to query so it can be built up
        self.query = self._querybase
        if len(self.fields) > 0:
            #add "and" keyword before adding in fields
            for field in self.fields:
                self.query = self.query + ' or ' + f'r._field == "{field}"'
        
        #add any tag filters
        if len(self.tags) > 0:
            for tag in self.tags:
                self.query = self.query + ' and ' + f'(r.tag == "{tag}"'
        
        #add closing )
        self.query = self.query + ')'

if __name__ == "__main__":
    bucket = 'home'
    time_range = -1
    measurement = 'home'
    fields = ['humidity', 'temperature']

    test_query = Query(bucket, time_range, measurement, fields=fields)
    print(test_query.query)

