import xmltodict
import pprint
import json
import urllib.request
import re
from whisper_transcribe import transcribe
import os


def format_transcription(item, result):
    title = 

def transcribe(paths):
    print('transcribing episode', paths['ep_number'])
    audio = whisper.load_audio(paths['audio'])
    audio = whisper.pad_or_trim(audio)
    
    result = model.transcribe(audio, verbose = True)

    with open(paths['whisper'], "w") as file:
        json.dump(result, file, indent=4)
    
    return result


def download_audio(paths):
    print('downloading episode', paths['ep_number'])
    urllib.request.urlretrieve(paths['url'], paths['audio'])

def extract_ep_from_title(title): 
    pattern = r'(?:ep(?:isode)?\s?)(\d+)'
    match = re.findall(pattern, title, re.IGNORECASE)
    if match:
        return str(match[0])
    return None

def make_paths_from_item(item):
    ep = extract_ep_from_title(item['title'])

    return  {
        'ep_number': ep, 
        'url': item['enclosure']['@url'],
        'audio': './episodes/' + ep + '.mp3',
        'transcript': './transcripts/' + ep + '.json',
        'whisper': './whisper-output/' + ep + '.json'
    }
    
def main():

    #open rss feed xml
    with open('rss.xml', 'r', encoding='utf-8') as file:
        rss_xml = file.read()

    #xml to dict
    rss = xmltodict.parse(rss_xml)

    #dump feed in rss.json
    with open("rss.json", "w") as file:
      json.dump(rss, file, indent=4)
  
    #load whisper model
    model = whisper.load_model("base")

    #process each item (episode) of the feed
    limit = 5
    for i, item in enumerate(rss['rss']['channel']['item']):
        if i > limit:
            break
        paths = make_paths_from_item(item)

        #download the mp3
        download_audio(paths)

        #transcribe with whisper
        result = transcribe(paths)

        #make mongo-ready
        format_transcript(item, result)

        #delete the mp3
        os.remove(paths['audio'])

      
if __name__ == "__main__":
    main()