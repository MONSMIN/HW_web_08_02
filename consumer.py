import pika
import src.connect
from src.models import Contact

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="host", port=5672, credentials=credentials,
                              virtual_host='user'))
channel = connection.channel()
channel.queue_declare(queue="email_queue")


def send_email(contact_id):
    contact = Contact.objects.get(id=contact_id)
    print(f'Sending email to {contact.email}...')
    # Тут треба функціонал надсилання email
    contact.is_sent = True
    contact.save()
    print(f'Email sent to {contact.email}')


def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects.get(id=contact_id)
    send_email(contact_id)
    contact.email_sent = True
    contact.save()

    print(f"Processed contact with ID: {contact_id}")


if __name__ == "__main__":
    channel.basic_consume(queue="email_queue", on_message_callback=callback, auto_ack=True)

    print("Consumer started")
    channel.start_consuming()
