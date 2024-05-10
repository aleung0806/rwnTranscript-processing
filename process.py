import xmltodict
from pprint import pprint
import json
import urllib.request
import re
import os
import whisperx
import time

device = "cpu" 
audio_file = "rwn.mp3"
batch_size = 4
compute_type = "int8"
language = "en"

log_path = 'process.log'

def log(message):
    with open(log_path, "a") as log_file:
        print(message)
        pprint(message, log_file)

def transcribe(ep_info, model):
    print('transcribing', ep_info['ep_number'])
    audio = whisperx.load_audio(ep_info['mp3_url'])
    result = model.transcribe(audio, batch_size=batch_size)

    with open(ep_info['transcript_path'], "w") as log_file:
        pprint(result, log_file)

    print(ep_info['ep_number'], 'transcribed')
    return result

    

def delete_mp3(ep_info):
    os.remove(ep_info['audio_path'])

def download_audio(paths):
    print('downloading episode', paths['ep_number'])
    urllib.request.urlretrieve(paths['mp3_url'], paths['audio_path'])

def extract_ep_from_title(title): 
    pattern = r'(?:ep(?:isode)?\s?)(\d+)'
    match = re.findall(pattern, title, re.IGNORECASE)
    if match:
        return str(match[0])
    return None

def extact_info_from_feed(item):
    ep = extract_ep_from_title(item['title'])

    return  {
        'ep_number': ep, 
        'mp3_url': item['enclosure']['@url'],
        'audio_path': './audio/' + ep + '.mp3',
        'transcript_path': './transcripts/' + ep + '.json'
    }
    
def main():

    os.remove(log_path)
    t = time.process_time()

    #open rss feed xml
    with open('feed.xml', 'r', encoding='utf-8') as file:
        rss_xml = file.read()

    #xml to dict
    rss = xmltodict.parse(rss_xml)

    #load whisper model
    model = whisperx.load_model("base", device, compute_type=compute_type, language=language)

    #process each episode

    t = time.process_time() - t
    log('model loaded: ' + str(t))
    limit = 5
    for i, item in enumerate(rss['rss']['channel']['item']):
        if i > limit:
            break

        ep_info = extact_info_from_feed(item)
        download_audio(ep_info)

        t = time.process_time() - t
        log('mp3 downloaded: ' + str(t))

        transcribe(ep_info, model)
        t = time.process_time() - t
        log('episode transcribed: ' + str(t))

        delete_mp3(ep_info)

      
if __name__ == "__main__":
    main()