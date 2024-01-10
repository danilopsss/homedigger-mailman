import os
import pickle
from uuid import uuid4
from pika import (
    BlockingConnection,
    ConnectionParameters,
    PlainCredentials,
    BasicProperties,
)

from pika.exceptions import ChannelClosedByBroker
from hdmailman.exceptions import VHostNotFoundException


class RabbitMQ:
    def __init__(self):
        self._host = os.getenv("BROKER_HOST", "HOST")
        self._port = os.getenv("BROKER_PORT", "0000")
        self._username = os.getenv("BROKER_USERNAME", "USERNAME")
        self._password = os.getenv("BROKER_PASSWORD", "PASSWORD")
        self._vhost = os.getenv("BROKER_VHOST", "VHOST")

    @property
    def rabbitmq(self) -> BlockingConnection:
        credentials = PlainCredentials(
            username=self._username, password=self._password
        )
        conn_params = ConnectionParameters(
            host=self._host,
            port=self._port,
            virtual_host=self._vhost,
            credentials=credentials,
        )
        return BlockingConnection(conn_params)

    def publish_message(
        self, message: str | bytes, exchange: str, route: str
    ) -> None:
        message_id = uuid4()
        serialized_message = pickle.dumps(message)
        try:
            with self.rabbitmq.channel() as channel:
                channel.basic_publish(
                    exchange=exchange,
                    routing_key=route,
                    body=serialized_message,
                    properties=BasicProperties(
                        message_id=str(message_id),
                    ),
                )
        except ChannelClosedByBroker as channer_err:
            raise VHostNotFoundException(channer_err.args[1])

    def start_consuming(self, queue: str, callback: callable) -> None:
        with self.rabbitmq.channel() as channel:
            channel.basic_consume(
                queue=queue, on_message_callback=callback, auto_ack=True
            )
            channel.start_consuming()
