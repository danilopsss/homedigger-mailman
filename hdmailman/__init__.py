from .brokers import Registry
from typing import Union


class MailMan:
    def __init__(self, broker: str):
        self._broken_name = broker
        self._broker = Registry.get_broker_conn(broker)()

    @property
    def broker(self):
        return self._broker
