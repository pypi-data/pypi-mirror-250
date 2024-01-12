# -*- coding: utf-8 -*-

from __future__ import absolute_import
from builtins import str
from builtins import object
import logging
import os
import json
import tornado.ioloop

from google.cloud import pubsub_v1

LOGGER = logging.getLogger(__name__)


class BaseConsumer(object):
    TOPIC_ID = None
    subscription_name = None
    is_running = False
    loop = None

    def __init__(self):
        self.subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
            project_id=os.getenv('PUBSUB_SUBSCRIBER_PROJECT_ID'),
            sub=self.TOPIC_ID
        )
        self.instance = pubsub_v1.SubscriberClient()
        self.loop = tornado.ioloop.IOLoop.current()

    def on_message(self, message_id, data, attributes, publish_time):
        pass

    def run(self):
        def handle_message(message):
            LOGGER.info('Received message # %s: %s, %s, %s' % (
                message.message_id, message.data, message.attributes, message.publish_time))

            try:
                self.on_message(message.message_id, json.loads(message.data),
                                message.attributes, message.publish_time)
                LOGGER.info('Acknowledging message %s', message.message_id)
                message.ack()
            except Exception as e:
                LOGGER.exception(
                    'Error occured when handling message: %s', str(e))
                message.nack()

        self.instance.subscribe(self.subscription_name, handle_message)

        self.loop.start()

    def stop(self):
        self.loop.stop()
