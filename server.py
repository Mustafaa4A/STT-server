from middleware.auth import verifyToken
from transcription.route import transcription
from auth.route import authenticate
from flask import Flask, request, jsonify, Blueprint, make_response
from flask_cors import CORS
from mongoengine import connect


app = Flask(__name__)
CORS(app)

# connect mongo db
connect(host="mongodb://127.0.0.1:27017/asr_web")


# register user
app.register_blueprint(authenticate)
app.register_blueprint(transcription)


@app.before_request
def parse_json():
  if request.content_type == "application/json":
    request.body = request.get_json()
  else:
    request.body = request.form.to_dict()


# @app.before_request
# def connect_to_database():
#   try:
#     connect()
#   except Exception as e:
#     raise Exception('Failed to connect to MongoDB: {}'.format(e))


@app.get("/")
@verifyToken
def index():
  return {
      "status": True,
      "data": "data_dict"
  }


@app.post("/")
@verifyToken
def get_index():
  # name = request.body["name"]
  return {
      "user": "request.user"
  }


@app.errorhandler(404)
def page_not_found_error(e):
  return jsonify({'message': 'The requested URL was not found on the server'}), 404


if __name__ == "__main__":
  app.run(debug=True, threaded=True)
