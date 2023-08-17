from config import *
import logging
import api.v1.events as events
import pika
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from notification.utils.logger import LOGGING
from mq import rmq

connection = None

app = FastAPI(
    title=PROJECT_NAME,
    description="Система для получения сообщений на API и отправки их на email",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    version="1.0.0"
)


@app.on_event('startup')
async def startup():
    """ Function for connecting RabbitMQ"""
    global connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST))
    rmq.channel = connection.channel()
    rmq.channel.queue_declare(queue=DEFAULT_QUEUE)
    print('TYPE 3 -', type(rmq.channel))


@app.on_event('shutdown')
async def shutdown():
    """ Function for disconnecting RabbitMQ"""
    global connection
    if isinstance(connection, pika.BlockingConnection):
        connection.close()

app.include_router(events.router, prefix='/v1/events', tags=['Events'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=APP_PORT,
        log_config=LOGGING,
        log_level=logging.DEBUG
    )
