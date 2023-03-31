from mongoengine import Document
from mongoengine.fields import StringField, BooleanField


class User(Document):
    fullname = StringField()
    email = StringField()
    received_a_message = BooleanField(default=False)
