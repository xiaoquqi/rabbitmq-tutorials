#!/usr/bin/env python

from kombu import Connection

connection = Connection('amqp://localhost//')

with connection.channel() as channel:
    channel.exchange_declare('logs', 'fanout')
    queue = channel.queue_declare(exclusive=False)
    queue_name = queue.queue

    # Connection.Channel.queue_bind(queue, exchange='', routing_key='', nowait=False, arguments=None)
    channel.queue_bind(queue_name, exchange='logs')
    print ' [*] Waiting for messages. To exit press CTRL+C'

    def callback(response):
        print " [x] Received %r" % (response.body,)


    channel.basic_consume(
            queue=queue_name,
            callback=callback,
            no_ack=True)

    while True:
        channel.wait()
