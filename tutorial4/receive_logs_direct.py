#!/usr/bin/env python

from kombu import Connection
import sys

severities = sys.argv[1:]
if not severities:
    print >> sys.stderr, "Usage: %s [info][warning][error]" % \
            (sys.argv[0], )
    sys.exit(1)

connection = Connection('amqp://localhost//')

with connection.channel() as channel:
    channel.exchange_declare('direct_logs', 'direct')
    queue = channel.queue_declare(exclusive=False)
    queue_name = queue.queue

    for severity in severities:
        # Connection.Channel.queue_bind(queue, exchange='', routing_key='', nowait=False, arguments=None)
        channel.queue_bind(queue_name,
                exchange='direct_logs',
                routing_key=severity)
    print ' [*] Waiting for messages. To exit press CTRL+C'

    def callback(response):
        print " [x] Received %r: %r" % (response.delivery_info['routing_key'], response.body,)

    channel.basic_consume(
            queue=queue_name,
            callback=callback,
            no_ack=True)

    while True:
        channel.wait()
