#!/bin/bash/env python

from kombu import Connection
import sys

routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
message = ''.join(sys.argv[2:]) or "Hello, World!"

connection = Connection('amqp://localhost//')

with connection.channel() as channel:
    channel.exchange_declare('topic_logs', 'topic')
    msg = channel.prepare_message(message)
    channel.basic_publish(msg, exchange='topic_logs', routing_key=routing_key)
    print "[x] Sending %r: %r" % (routing_key, message)
