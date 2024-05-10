import xmltodict
import json

def main():

    #open rss feed xml
    with open('rss.xml', 'r', encoding='utf-8') as file:
        rss_xml = file.read()

    #xml to dict
    rss = xmltodict.parse(rss_xml)

    #dump feed in rss.json
    with open("rss.json", "w") as file:
      json.dump(rss, file, indent=4)

      
if __name__ == "__main__":
    main()