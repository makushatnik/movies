import pika
import json
from notification.models.events import Event, EventEncoder
from fastapi import APIRouter, Depends
from .response import ApiResponse
from time import sleep
from http import HTTPStatus
from notification.config import *

from notification.services.events import EventService, get_event_service

router = APIRouter()


@router.post('/send/immediate', response_model=ApiResponse)
async def send_immediate(event: Event, service: EventService = Depends(get_event_service)) -> ApiResponse:
    """ Function for immediate sending a Message to RabbitMQ """
    return await send(event)


@router.post('/send/deferred', response_model=ApiResponse)
async def send_deferred(event: Event, deferred_time: int,
                        service: EventService = Depends(get_event_service)) -> ApiResponse:
    """ Function for deferred sending a Message to RabbitMQ """
    if deferred_time > 0:
        sleep(deferred_time)
    return await service.send(event)


async def send(event: Event) -> ApiResponse:
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST))
    channel = connection.channel()
    json_data = json.dumps(event, cls=EventEncoder)
    channel.basic_publish(exchange='',
                          routing_key=DEFAULT_QUEUE,
                          body=json_data.encode(ENCODING),
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          )
    )
    print(" [x] Message Sent")
    connection.close()
    return ApiResponse(result=['ok'], status=HTTPStatus.OK, errors=[])
