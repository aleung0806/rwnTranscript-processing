import whisperx
import gc 
from pprint import pprint
import time
import os
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv('HF_TOKEN')

device = "cpu" 
audio_file = "443.mp3"
batch_size = 4
compute_type = "int8"
language="en"

t = time.process_time()

model = whisperx.load_model("small", device, compute_type=compute_type, language=language)

t = time.process_time() - t
pprint(t)


audio = whisperx.load_audio(audio_file)
result = model.transcribe(audio, batch_size=batch_size)

t = time.process_time() - t
pprint(t)

# diarize_model = whisperx.DiarizationPipeline(use_auth_token=HF_TOKEN, device=device)
# diarize_segments = diarize_model(audio, min_speakers=1, max_speakers=4)
# result = whisperx.assign_word_speakers(diarize_segments, result)

with open("results", "w") as log_file:
    pprint(result, log_file)


