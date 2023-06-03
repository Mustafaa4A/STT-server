from flask import Blueprint, request, make_response
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from .model import User
from .controller import get_user
from mongoengine.errors import ValidationError, NotUniqueError

load_dotenv()

authenticate = Blueprint('auth', __name__, url_prefix='/auth')


@authenticate.post('/login')
def login():
  username, password, *_ = request.body.values()
  if not username or not password:
    return {"status": False, "message": "Missing required Arguments"}, 400

  user = get_user(username=username)

  if not user:
    return {"status": False, "message": "Invalid user"}, 400
  if not user.authenticate(password):
    return {"status": False, "message": "Invalid password"}, 400

  token = jwt.encode({
      "user":  user.to_dict(),
      'expiration': str(datetime.utcnow() + timedelta(seconds=5))
  },
      os.environ['SECRET_KEY']
  )

  return {
      "status": True,
      "data": {
          "user": user.to_dict(),
          "token": token
      }
  }


@authenticate.post("/register")
def register():
  try:
    name, username, password, *_ = request.body.values()
    if not name or not username or not password:
      return {"status": False, "message": "Missing required Arguments"}, 400

    user = User(fullname=name, username=username, password=password)
    user.save()

    return {
        "status": True,
        "data": user.to_dict()
    }
  except ValidationError as error:
    return {"status": False, "message": str(error)}, 400

  except NotUniqueError as error:
    return {"status": False, "message": "The username already exists"}, 400

  except Exception as error:
    return {"status": False, "message": error}, 400
