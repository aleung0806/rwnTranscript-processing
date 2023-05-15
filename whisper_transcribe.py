import whisper
import json

model = whisper.load_model("base")

def transcribe(paths):
  print('transcribing episode', paths['ep_number'])
  audio = whisper.load_audio(paths['audio'])
  audio = whisper.pad_or_trim(audio)
  
  result = model.transcribe(paths['audio'], verbose = True)

  with open(paths['transcript'], "w") as file:
    json.dump(result, file)