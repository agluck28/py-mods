from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS


'''
Wraps the python influxDB client to make reading and writing a little
easier. This is intended to be expanded in a Writer and Reader class to help 
with increaded functionality 
'''

class Flux():
    '''
    will open the connection and also handle the writes
    '''
    def __init__(self, token, org, db_url):

        self.client = InfluxDBClient(url=db_url, token=token)
        
        self.org = org

    def Close(self):
        self.client.close()

class Writer(Flux):
    
    def __init__(self, token, org, db_url, bucket):
        #create writer that can be reused, inherits the client from the parent
        Flux.__init__(self, token, org, db_url)
        self.bucket = bucket
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def write_data(self, point):
        self.write_api.write(self.bucket, self.org, point)

    def Close(self):
        #close out writer and also insure the parent is called
        self.write_api.close()
        Flux.Close(self)

class Reader(Flux):

    def __init__(self, token, org, db_url):

        Flux.__init__(self, token, org, db_url)
        self.queryapi = self.client.query_api()

    def read_data(self, query):
        return self.queryapi.query(query, self.org)

def parse_table(table):
    '''
    Returns a list of time, value tuples based off the
    passed in table
    '''
    values = {
        'times': [],
        'data': []
    }
    for record in table:
        values['name'] = record['_field']
        values['times'].append(record['_stop'].isoformat())
        values['data'].append(record['_value'])
    return values

if __name__ == "__main__":
    pass