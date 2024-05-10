import whisperx
import gc 
from pprint import pprint
import time
import os
from dotenv import load_dotenv
import concurrent.futures
import faster_whisper
import whisperx
import json



num_workers = 4

file_paths = [
    "1.mp3",
    "2.mp3",
    "3.mp3",
    "4.mp3"
]

def transcribe(path):
    audio = whisperx.load_audio(path)
    print('transcribing ' + path)
    segments, info = model.transcribe(
        audio, 
        language="en"
    )
   
    results = []

    for segment in segments:
        s = dict(id = segment.id, text = segment.text, start = segment.start)
        results.append(s)

    with open('./transcripts/' + path + '.json', "w") as out:
        json.dump(results, out, indent=2)
    
    return results

model = faster_whisper.WhisperModel(
    "small", 
    device="cpu", 
    compute_type="int8", 
    num_workers=4, 
    cpu_threads=4
)


t = time.process_time()
# transcribe("1.mp3")
# print(time.process_time() - t)


with concurrent.futures.ThreadPoolExecutor(num_workers) as executor:
    results = executor.map(transcribe, file_paths)

    for file, result in zip(file_paths, results):
        print(file)

    print(time.process_time() - t)



