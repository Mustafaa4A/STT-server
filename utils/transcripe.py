import os
import speech_recognition as sr
from utils.convert_to_wave import convert_to_wav


# Create a speech recognition object
recognizer = sr.Recognizer()


def stt(audio):
  # convert file audio into wave
  converted_audio = convert_to_wav(audio)

  # Get the filename of the converted audio
  wav_filename = "converted_audio.wav"
  converted_audio.export(wav_filename, format="wav")

  # Open the audio file
  with sr.AudioFile(wav_filename) as source:
    audio_data = recognizer.record(source)

  # Transcribe the audio
  transcript = recognizer.recognize_google(audio_data)

  # Delete the temporary WAV file
  os.remove(wav_filename)

  return transcript
