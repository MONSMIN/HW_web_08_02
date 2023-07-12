import pika
import src.connect
from faker import Faker
from src.models import Contact

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="host", port=5672, credentials=credentials,
                              virtual_host='user'))
channel = connection.channel()
channel.queue_declare(queue="email_queue")

fake = Faker()


def generate_fake_contacts(num_contacts):
    contacts = []
    for _ in range(num_contacts):
        full_name = fake.name()
        email = fake.email()
        contact = Contact(full_name=full_name, email=email)
        contact.save()
        contacts.append(contact)
    return contacts


def send_contacts_to_queue(contacts):
    for contact in contacts:
        channel.basic_publish(exchange="", routing_key="email_queue", body=str(contact.id).encode())
        print(f"Contact with ID {contact.id} sent to queue")


if __name__ == "__main__":
    fake_contacts = generate_fake_contacts(10)

    send_contacts_to_queue(fake_contacts)

    print("Contacts sent to queue")
    connection.close()
