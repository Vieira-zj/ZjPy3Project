# -*- coding: utf-8 -*-
'''
Created on 2019-01-08
@author: zhengjin

Condition: 
1) kafka libs: pip3 install kafka-python 
2) add /etc/hosts: 127.0.0.1 zjmbp

Reference:
https://kafka-python.readthedocs.io/en/latest/usage.html
'''

import json
import random
import threading
import time

from kafka import KafkaConsumer
from kafka import KafkaProducer


def process_producer(topic, server):
    def _on_send_sucess(record_metadata):
        print('send message success.')
        print('meta topic:', record_metadata.topic)
        print('meta partition:', record_metadata.partition)
        print("offset:", record_metadata.offset)

    def _on_send_failed(excp):
        print('send message failed:', excp)

    print('producer send msg ...')
    producer = None
    try:
        producer = KafkaProducer(
            bootstrap_servers=[server],
            value_serializer=lambda m: json.dumps(m).encode('utf-8'))
        for i in range(10):
            msg_dict = {
                'index': str(i + random.randint(1, 100)),
                'stat': 'ok',
            }
            future = producer.send(topic, value=msg_dict)
            future.add_callback(_on_send_sucess).add_errback(_on_send_failed)
    finally:
        if producer is not None:
            producer.flush()
            producer.close()
            print('close producer session.')


def process_consumer(topic, server):
    print('consumer receive msg ...')
    consumer = None
    try:
        consumer = KafkaConsumer(
            topic, bootstrap_servers=[server],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        for msg in consumer:
            recv_msg = "msg => %s:%d:%d: key=%s value=%s" % (
                msg.topic, msg.partition, msg.offset, msg.key, msg.value)
            print(recv_msg)
    finally:
        if consumer is not None:
            consumer.close()
            print('close consumer session.')


if __name__ == '__main__':

    topic = 'topic'
    server = 'zjmbp:9094'

    p1 = threading.Thread(target=process_producer, args=(topic, server))
    p2 = threading.Thread(target=process_producer, args=(topic, server))
    c1 = threading.Thread(target=process_consumer, args=(topic, server))

    # consumer
    c1.start()
    time.sleep(2)
    # producer1
    p1.start()
    p1.join()
    time.sleep(2)
    # producer2
    p2.start()
    p2.join()

    print('kafka test demo done.')
