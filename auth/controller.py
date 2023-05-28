from .model import User
from mongoengine.errors import DoesNotExist


def get_user(username):
  try:
    user = User.objects.get(username=username)
    return user
  except DoesNotExist:
    return None
