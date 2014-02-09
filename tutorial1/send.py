#!/usr/bin/env python

from kombu import Connection

connection = Connection('amqp://localhost//')

with connection.channel() as channel:
    channel.queue_declare('hello')
    # Prepares message so that it can be sent using this transport.
    # http://kombu.readthedocs.org/en/latest/reference/kombu.transport.pyamqp.html#kombu.transport.pyamqp.Channel.Message
    msg = channel.prepare_message('Hello, World')
    channel.basic_publish(msg, exchange='', routing_key='hello')
    print " [x] Sent 'Hello World!'"
