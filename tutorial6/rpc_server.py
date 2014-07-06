#!/usr/bin/python

from kombu import Connection, Producer
import sys
import ipdb

connection = Connection('amqp://localhost//')

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def on_request(request):
    #ipdb.set_trace()
    n = int(request.body)

    print " [.] fib(%s)"  % (n,)
    result = fib(n)
    print "Result is", result

    producer = Producer(request.channel)
    producer.publish(
            str(result),
            exchange='',
            routing_key=request.properties['reply_to'],
            correlation_id=request.properties['correlation_id'])
    request.channel.basic_ack(request.delivery_info['delivery_tag'])

with connection.channel() as channel:
    channel.queue_declare(queue='rpc_queue', exclusive=False)

    channel.basic_qos(0, 1, False)

    channel.basic_consume(queue='rpc_queue', callback=on_request)

    print " [x] Awaiting RPC requests"
    while True:
        channel.wait()
