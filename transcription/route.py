from flask import Blueprint, request
from utils.transcripe import stt

#
from middleware.auth import verifyToken


transcription = Blueprint("transcription", __name__, url_prefix="/transcripe")


@transcription.get("/")
@verifyToken
def index():
  return {
      "status": True
  }


@transcription.post("/")
@verifyToken
def upload():
  name = request.form["name"]
  file = request.files["file"]

  text = stt(audio=file)

  return {
      "status": True,
      "name": name,
      "file": text
  }
