#!/usr/bin/env python

from kombu import Connection
import time

connection = Connection('amqp://localhost//')

with connection.channel() as channel:
    channel.queue_declare('task_queue', durable=True)
    print ' [*] Waiting for messages. To exit press CTRL+C'

    def callback(response):
        print " [x] Received %r" % (response.body,)
        time.sleep(len(response.body))
        print '[x] Done'
        response.channel.basic_ack(response.delivery_info['delivery_tag'])

    # http://kombu.readthedocs.org/en/latest/reference/kombu.transport.pyamqp.html?highlight=basic_qos#kombu.transport.pyamqp.Connection.Channel.basic_qos
    # Connection.Channel.basic_qos(prefetch_size, prefetch_count, a_global)
    # Fair dispatch
    channel.basic_qos(0, 1, False)

    channel.basic_consume(queue='task_queue', callback=callback)

    while True:
        channel.wait()
