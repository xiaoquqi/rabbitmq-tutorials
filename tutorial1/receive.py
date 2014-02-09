#!/usr/bin/env python

from kombu import Connection

connection = Connection('amqp://localhost//')

with connection.channel() as channel:
    channel.queue_declare('hello')
    print ' [*] Waiting for messages. To exit press CTRL+C'

    def callback(response):
        print " [x] Received %r" % (response.body,)

    channel.basic_consume(queue='hello', no_ack=True, callback=callback)

    while True:
        channel.wait()
