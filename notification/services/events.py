import json
import pika
from pika.adapters.blocking_connection import BlockingChannel
from functools import lru_cache
from fastapi import Depends
from notification.api.v1.response import ApiResponse
from notification.config import *
from notification.models.events import Event
from http import HTTPStatus
from notification.mq.rmq import get_channel


class EventService:
    def __init__(self, channel: BlockingChannel):
        self.channel = channel

    async def send(self, event: Event) -> ApiResponse:
        if not self.channel:
            err = "Channel isn't set"
            print(err)
            return ApiResponse(result=[], status=HTTPStatus.INTERNAL_SERVER_ERROR, errors=[err])

        self.channel.basic_publish(exchange='',
                                   routing_key=DEFAULT_QUEUE,
                                   body=json.dumps(event).encode(ENCODING),
                                   properties=pika.BasicProperties(
                                       delivery_mode=2,  # make message persistent
                                   )
        )
        print(" [x] Message Sent")
        return ApiResponse(result=['ok'], status=HTTPStatus.OK, errors=[])


@lru_cache()
def get_event_service(channel: BlockingChannel = Depends(get_channel)) -> EventService:
    return EventService(channel)
