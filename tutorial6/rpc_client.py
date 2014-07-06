#!/usr/bin/python

from kombu import Connection, Producer
import sys
import uuid
import ipdb


class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = Connection('amqp://localhost//')
        self.channel = self.connection.channel()
        self.response_queue = self.channel.queue_declare(exclusive=True)

        self.channel.basic_consume(
                queue=self.response_queue.queue,
                callback=self.on_response,
                no_ack=True)

    def on_response(self, response):
        '''consume callback'''
        correlation_id = response.properties['correlation_id']
        if correlation_id == self.corr_id:
            self.response = response.body

    def call(self, n):
        #ipdb.set_trace()
        self.response = None
        self.corr_id = str(uuid.uuid4())
        producer = Producer(self.connection)
        producer.publish(
                str(n),
                exchange='',
                routing_key='rpc_queue',
                reply_to=self.response_queue.queue,
                correlation_id=self.corr_id)

        # FIXME(Ray): if we use pika this should be
        # self.connection.process_data_events()
        # But in kombu I can not find one for this
        if self.response is None:
            self.connection.drain_events()

        return int(self.response)

fibonacci_rpc = FibonacciRpcClient()

print " [x] Requesting fib(30)"
response = fibonacci_rpc.call(30)
print " [.] Got %r" % (response,)
