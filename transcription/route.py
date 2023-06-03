from flask import Blueprint, request
from utils.transcripe import stt

#
from middleware.auth import verifyToken


transcription = Blueprint("transcription", __name__, url_prefix="/transcribe")


@transcription.get("/")
@verifyToken
def index():
  return {
      "status": True
  }


@transcription.post("/")
@verifyToken
def upload():
  file = request.files["file"]

  try:
    text = stt(audio=file)
  except Exception as err:
    return {
        "status": False,
        "message": str(err)
    }

  if not text:
    return {"status": False, "message": "Process Failed"}, 400

  return {
      "status": True,
      "data": text
  }
