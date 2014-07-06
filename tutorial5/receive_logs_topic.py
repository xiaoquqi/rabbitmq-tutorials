#!/usr/bin/env python

from kombu import Connection
import sys

binding_keys = sys.argv[1:]
if not binding_keys:
    print >> sys.stderr, "Usage: %s [binding_key]..." % (sys.argv[0],)
    sys.exit(1)

connection = Connection('amqp://localhost//')

with connection.channel() as channel:
    channel.exchange_declare('topic_logs', 'topic')
    queue = channel.queue_declare(exclusive=False)
    queue_name = queue.queue

    for binding_key in binding_keys:
        # Connection.Channel.queue_bind(queue, exchange='', routing_key='', nowait=False, arguments=None)
        channel.queue_bind(queue_name,
                exchange='topic_logs',
                routing_key=binding_key)
    print ' [*] Waiting for messages. To exit press CTRL+C'

    def callback(response):
        print " [x] Received %r: %r" % (response.delivery_info['routing_key'], response.body,)

    channel.basic_consume(
            queue=queue_name,
            callback=callback,
            no_ack=True)

    while True:
        channel.wait()
