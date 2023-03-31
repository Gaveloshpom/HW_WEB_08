import time
import pika

import connect
from models import User

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue="task_queue_100", durable=True)
print(" [*] Waiting for messages. To exit press CTRL+C")


def callback(ch, method, properties, body):
    message = body.decode()
    print(f" [x] Received {body}")
    user = User.objects(id=message)
    user.update(received_a_message=True)
    time.sleep(1)
    print("Повідомлення відправлено")


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="task_queue_100", on_message_callback=callback, auto_ack=True)


if __name__ == '__main__':
    channel.start_consuming()
