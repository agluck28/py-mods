'''
Wrapper around the Pika library to help abstract away 
making the exchange connections and handling the routing keys
'''

import pika
import json


class Rabbit():
    '''
    Handles opening the connection to the exchange, declaring the exhanges and expose
    methods to receive data or send messages to the exchange. This only supports topic 
    exchanges
    '''

    def __init__(self, rabbitUrl, exchange, routing_keys):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(rabbitUrl))
            self.channel = self.connection.channel()
            self.channel.exchange_declare(
                exchange=exchange, exchange_type='topic')
            self.exchange = exchange
            self.routing_keys = routing_keys
        except Exception as e:
            print(e)

    def close(self):
        self.connection.close()

    def send_message(self, message):
        '''
        Sends Python dictonary to the exchange
        '''
        try:
            for key in self.routing_keys:
                self.channel.basic_publish(exchange=self.exchange,
                                           routing_key=key,
                                           body=json.dumps(message),
                                           properties=pika.BasicProperties(
                                               delivery_mode= 2,
                                           ))
        except Exception as e:
            print(e)
            return -1

    def start_listening(self, callback):
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        # bind the queues to the routing keys
        for key in self.routing_keys:
            self.channel.queue_bind(exchange=self.exchange,
                                    queue=queue_name,
                                    routing_key=key)

        self.channel.basic_consume(queue=queue_name,
                                   on_message_callback=callback,
                                   auto_ack=True)
        self.channel.start_consuming()

    
