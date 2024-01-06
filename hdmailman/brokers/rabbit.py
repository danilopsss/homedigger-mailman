import os
from uuid import uuid4
from pika import (
    BlockingConnection,
    ConnectionParameters,
    PlainCredentials,
    BasicProperties,
)
from pika.connection import BlockingConnection


class RabbitMQ:

    def __init__(self):
        self._host = os.getenv("BROKER_HOST", "HOST")
        self._port = os.getenv("BROKER_PORT", "0000")
        self._username = os.getenv("BROKER_USERNAME", "USERNAME")
        self._password = os.getenv("BROKER_PASSWORD", "PASSWORD")

    @property
    def rabbitmq(self) -> BlockingConnection:
        credentials = PlainCredentials(
            username=self._username,
            password=self._password
        ) 
        conn_params = ConnectionParameters(
            host=self._host,
            port=self._port,
            credentials=credentials
        )
        return BlockingConnection(conn_params)

    def publish_message(self, message: str | bytes, exchange: str, route: str) -> None:
        message_id = uuid4()
        with self.rabbitmq.channel() as channel:
            channel.basic_publish(
                exchange=exchange,
                routing_key=route,
                body=message,
                properties=BasicProperties(
                    message_id=str(message_id),
                )
            )

    def start_consuming(self, queue: str, callback: callable) -> None:
        with self.rabbitmq.channel() as channel:
            channel.basic_consume(
                queue=queue,
                on_message_callback=callback,
                auto_ack=True
            )
            channel.start_consuming()
