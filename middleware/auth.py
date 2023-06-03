from functools import wraps
from flask import request
import jwt
from dotenv import load_dotenv
import os

load_dotenv()


def verifyToken(func):
  @wraps(func)
  def decorated(*args, **kwargs):
    token = request.headers.get('token')
    if not token:
      return {"status": False, "message": "Authentication required"}, 403
    try:
      verified = jwt.decode(
          token, os.environ['SECRET_KEY'], algorithms=['HS256'])
      request.user = verified["user"]
    except jwt.ExpiredSignatureError:
      return {"status": False, 'message': 'Token has expired.'}, 401
    except:
      return {"status": False, "message": "Invalid Authentication"}, 403

    return func(*args, **kwargs)
  return decorated
