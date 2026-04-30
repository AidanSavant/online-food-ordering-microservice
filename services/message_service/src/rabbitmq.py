import os
import aio_pika

async def get_connection() -> aio_pika.abc.AbstractConnection:
    url = os.getenv("RABBITMQ_URL")
    if not url:
        raise RuntimeError("Failed to get connection! Reason: RABBITMQ_URL env var must be set!")

    return await aio_pika.connect_robust(url)

async def publish_msg(msg: str) -> str:
    connection = await get_connection()

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("msg_queue", durable=True)

        await channel.default_exchange.publish(
            aio_pika.Message(body=msg.encode()),
            routing_key="msg_queue"
        )

        async with queue.iterator() as queue_iter:
            async for recv_msg in queue_iter:
                async with recv_msg.process():
                    return recv_msg.body.decode()

    return msg
