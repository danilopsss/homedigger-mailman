from .brokers import Registry
from typing import Union


class MailMan:

    def __init__(self, broker: str):
        self._broken_name = broker
        self._broker = Registry.get_broker_conn(broker)()

    @property
    def broker(self) :
        return getattr(self._broker, self._broken_name)

    def dispatch_message(self, function) -> dict:
        def dispatch(*args, **kwargs):
            message = function(*args, **kwargs)
            with (channel := self.broker.channel()):
                channel.basic_publish(
                    exchange=message.get("exchange", "file.created"),
                    routing_key=message.get("routing_key", "file.created"),
                    body=message.get("file", ""),
                    properties=BasicProperties(
                        message_id=str(uuid4()),
                    )
                )
            message.pop("broker")
            return args
            # return jsonify(message), 202
        return dispatch
