import xmltodict
import pprint
import json
import urllib.request
import re
from whisper_transcribe import transcribe

def download_audio(paths):
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
        'transcript': './transcripts/' + ep + '.json'
    }
    
def main():

    with open('rss.xml', 'r', encoding='utf-8') as file:
        rss_xml = file.read()

    rss = xmltodict.parse(rss_xml)

    with open("rss.json", "w") as file:
      json.dump(rss, file)
  
    limit = 5
    for i, item in enumerate(rss['rss']['channel']['item']):
        if i > limit:
            break
        paths = make_paths_from_item(item)
        download_audio(paths)
        transcribe(paths)
      
if __name__ == "__main__":
    main()