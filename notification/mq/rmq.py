from pika.adapters.blocking_connection import BlockingChannel

channel: BlockingChannel = None


async def get_channel() -> BlockingChannel:
    return channel
