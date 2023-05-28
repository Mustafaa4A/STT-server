import io
import os
from pydub import AudioSegment


def convert_to_wav(audio_file):
  """
  Converts an audio file from a file object to WAV format using the pydub library,
  and returns the converted audio as an AudioSegment object.

  Args:
      audio_file (FileStorage): The audio file as a file object.

  Returns:
      audio (AudioSegment): The converted audio as an AudioSegment object.
  """
  # Load the audio file as an AudioSegment object
  audio = AudioSegment.from_file(io.BytesIO(audio_file.read()))

  # Export the audio file as WAV to a BytesIO object
  wav_buffer = io.BytesIO()
  audio.export(wav_buffer, format="wav")

  # Load the exported WAV file as an AudioSegment object
  wav_audio = AudioSegment.from_file(
      io.BytesIO(wav_buffer.getvalue()), format="wav")

  return wav_audio
