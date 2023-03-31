import pika
from faker import Faker

import connect
from models import User

fake = Faker()

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='exchange')
channel.queue_declare(queue="task_queue_100", durable=True)
channel.queue_bind(exchange="exchange", queue="task_queue_100")


def main():
    for i in range(10):
        User(fullname=fake.name(), email=fake.email()).save()
        channel.basic_publish(exchange="exchange", routing_key="task_queue_100", body=f"{[n.id for n in User.objects()][i]}".encode())
    connection.close()


if __name__ == "__main__":
    main()
