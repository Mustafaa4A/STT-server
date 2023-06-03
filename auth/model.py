
from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import *
import datetime
from mongoengine.signals import pre_save


class User(Document):
  fullname = StringField(required=True,  min_length=3, max_length=200)
  username = StringField(required=True, unique=True,
                         min_length=4, max_length=50)
  password = StringField(required=True)
  tokens = IntField(default=1000)
  created_date = DateTimeField(default=datetime.datetime.now())

  # Define a pre_save signal handler to encrypt the password
  @classmethod
  def encrypt_password(cls, sender, document, **kwargs):
    document.password = generate_password_hash(document.password)

  def authenticate(self, password):
    """Returns True if the password is correct, False otherwise."""
    return check_password_hash(self.password, password)

  def to_dict(self):
    return {
        "fullname": self.fullname,
        "username": self.username,
        "tokens": self.tokens
    }

  def __str__(self):
    return self.username

  # Set the collection name to 'users'
  meta = {'collection': 'users'}


pre_save.connect(User.encrypt_password, sender=User)
