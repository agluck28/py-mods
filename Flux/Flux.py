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
    def __init__(self, token, org, bucket, db_url):

        self.client = InfluxDBClient(url=db_url, token=token)
        self.bucket = bucket
        self.org = org

    def Close(self):
        self.client.close()

class Writer(Flux):
    
    def __init__(self, token, org, bucket, db_url):
        #create writer that can be reused, inherits the client from the parent
        Flux.__init__(self, token, org, bucket, db_url)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def write_data(self, point):
        self.write_api.write(self.bucket, self.org, point)

    def Close(self):
        #close out writer and also insure the parent is called
        self.write_api.close()
        Flux.Close(self)