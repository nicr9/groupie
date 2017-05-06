import requests
import os

from urllib.parse import urljoin
from flask import Flask, render_template, request

app = Flask(__name__)

BASE_URL = "https://app.ticketmaster.com/"

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY", None)
if not TICKETMASTER_API_KEY:
    print(USAGE)
    exit(1)


# Helper methods

def search_attractions(keyword, locale='en-ie'):
    url = urljoin(BASE_URL, '/discovery/v2/attractions.json')
    resp = requests.get(url, params={
        'apikey': TICKETMASTER_API_KEY,
        'keyword': keyword,
        })

    return resp.json()

def attraction_details(attraction_id):
    url = urljoin(BASE_URL, '/discovery/v2/attractions/{}.json'.format(attraction_id))
    resp = requests.get(url, params={
        'apikey': TICKETMASTER_API_KEY,
        })

    return resp.json()

# TODO: Take country_code as a param
def attraction_events(attraction_id, locale='en-ie'):
    url = urljoin(BASE_URL, '/discovery/v2/events.json')
    resp = requests.get(url, params={
        'apikey': TICKETMASTER_API_KEY,
        'attractionId': attraction_id,
        'countryCode': 'US',
        })

    return resp.json()

## Routes

@app.route('/', methods=['GET'])
def homepage():
    return render_template('homepage.html')

@app.route('/attractions', methods=['GET'])
def attractions():
    results = search_attractions(request.args.get('q'))
    return render_template('attractions.html', attractions=results['_embedded']['attractions'])

@app.route('/events/<attraction_id>', methods=['GET'])
def events(attraction_id):
    attr = attraction_details(attraction_id)
    results = attraction_events(attraction_id)
    evs = results['_embedded']['events'] if results['page']['totalElements'] else []
    return render_template('events.html', attr=attr, events=evs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
