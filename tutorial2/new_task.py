#!/bin/bash/env python

from kombu import Connection
import sys

message = ''.join(sys.argv[1:]) or "Hello, World!"

connection = Connection('amqp://localhost//')

with connection.channel() as channel:
    # When RabbitMQ quits or crashes it will forget the queues and
    # messages unless you tell it not to. Two things are required to make
    # sure that messages aren't lost:
    # we need to mark both the queue and messages as durable.
    #
    # durable: existing for a long time
    channel.queue_declare('task_queue', durable=True)
    msg = channel.prepare_message(message)
    channel.basic_publish(msg, exchange='', routing_key='task_queue')
