from functools import wraps
from flask import request, make_response, jsonify
import jwt
from dotenv import load_dotenv
import os

load_dotenv()


def verifyToken(func):
  @wraps(func)
  def decorated(*args, **kwargs):
    token = request.headers.get('token')
    if not token:
      return jsonify({"message": "Authentication required"}), 403
    try:
      verified = jwt.decode(
          token, os.environ['SECRET_KEY'], algorithms=['HS256'])
      request.user = verified["user"]
    except jwt.ExpiredSignatureError:
      return jsonify({'message': 'Token has expired.'}), 401
    except:
      return jsonify({"message": "Invalid Authentication"}), 403

    return func(*args, **kwargs)
  return decorated
