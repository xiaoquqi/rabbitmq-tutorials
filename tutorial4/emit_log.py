#!/bin/bash/env python

from kombu import Connection
import sys

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ''.join(sys.argv[1:]) or "Hello, World!"

connection = Connection('amqp://localhost//')

with connection.channel() as channel:
    channel.exchange_declare('direct_logs', 'direct')
    msg = channel.prepare_message(message)
    channel.basic_publish(msg, exchange='direct_logs', routing_key=severity)
    print "[x] Sending %r: %r" % (severity, message)
