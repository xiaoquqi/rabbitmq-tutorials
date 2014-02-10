#!/bin/bash/env python

from kombu import Connection
import sys

message = ''.join(sys.argv[1:]) or "Hello, World!"

connection = Connection('amqp://localhost//')

with connection.channel() as channel:
    channel.exchange_declare('logs', 'fanout')
    msg = channel.prepare_message(message)
    channel.basic_publish(msg, exchange='logs', routing_key='')
    print "[x] Sending %r" % (message, )
