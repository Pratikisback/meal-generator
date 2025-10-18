import pika
import time

def connect_rabbitmq(retries=5, delay=5):
    for i in range(retries):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = connection.channel()
            print("Connected to RabbitMQ")
            return connection, channel
        except pika.exceptions.AMQPConnectionError:
            print(f"RabbitMQ not ready, retrying in {delay} seconds...")
            time.sleep(delay)
    raise Exception("Could not connect to RabbitMQ after several retries")


