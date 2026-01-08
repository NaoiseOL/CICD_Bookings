import aio_pika
import json
import os

EXCHANGE_NAME = "bookings_events_topic"
RABBIT_URL = os.getenv("RABBIT_URL")

async def get_exchange():
    conn = await aio_pika.connect_robust(RABBIT_URL)
    ch = await conn.channel()
    ex = await ch.declare_exchange(EXCHANGE_NAME, aio_pika.ExchangeType.TOPIC)
    return conn, ch, ex

async def publish_event(event_type: str, payload: dict):
    print("PUBLISH CALLED", flush=True)
    conn,ch,ex = await get_exchange()

    msg = aio_pika.Message(
        body = json.dumps(payload).encode()
    )

    print("Publishing event:", event_type, payload)
    await ex.publish(msg, routing_key=event_type)
    await conn.close()