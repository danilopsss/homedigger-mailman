from .rabbit import RabbitMQ

class Registry:

    @classmethod
    def get_broker_conn(cls, broker: str):
        match broker:
            case "rabbitmq":
                return RabbitMQ
            case "kafka":
                raise NotImplementedError("Kafka not implemented")
            case _:
                raise ValueError("Broker not supported")
