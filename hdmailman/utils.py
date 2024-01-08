import os
from pika import BlockingConnection, ConnectionParameters, PlainCredentials


class Broker:

    def __init__(self):
        self.host = os.environ.get("BROKER_HOST")
        self.port = os.environ.get("BROKER_PORT")
        self.username = os.environ.get("BROKER_USERNAME")
        self.password = os.environ.get("BROKER_PASSWORD")

    @property
    def rabbitmq(self) -> ConnectionParameters:
        credentials = PlainCredentials(
            username=self.username,
            password=self.password
        ) 
        conn_params = ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=credentials
        )
        return BlockingConnection(conn_params)
