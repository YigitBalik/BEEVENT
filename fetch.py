import requests
import json
from config import APIKEY

root = 'https://app.ticketmaster.com/discovery/v2/'
fetchDict = {
    'events': 'events.json',
    'images': 'images.json',
    'venues': 'venues.json'
}
url = root + fetchDict['events'] + '?size=200&sort=random&apikey=' + APIKEY

payload = {}
headers = {}


def fetch():
    print('FETCH OPERATION')
    response = json.loads(requests.request(
        "GET", url, headers=headers, data=payload).text)
    events = response['_embedded']['events']
    with open('data.json', 'w', encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=4)