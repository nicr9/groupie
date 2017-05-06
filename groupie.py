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

def get_attraction_details(attraction_id):
    url = urljoin(BASE_URL, '/discovery/v2/attractions/{}.json'.format(attraction_id))
    resp = requests.get(url, params={
        'apikey': TICKETMASTER_API_KEY,
        })

    return resp.json()

def get_event_details(event_id):
    url = urljoin(BASE_URL, '/discovery/v2/events/{}.json'.format(event_id))
    resp = requests.get(url, params={
        'apikey': TICKETMASTER_API_KEY,
        })

    return resp.json()

def get_bookings(event):
    url = "https://api.airbnb.com/v2/search_results"
    resp = requests.get(url, params={
        'client_id': '3092nxybyb0otqw18e8nh5nty',
        'locale': 'en-US',
        'currency': 'USD',
        'guests': 1,
        'location': event['dates']['timezone'],
        'sort': 1,
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
    attr = get_attraction_details(attraction_id)
    results = attraction_events(attraction_id)
    evs = results['_embedded']['events'] if results['page']['totalElements'] else []
    return render_template('events.html', attr=attr, events=evs)

@app.route('/events/bookings/<event_id>', methods=['GET'])
def events_bookings(event_id):
    ev = get_event_details(event_id)
    results = get_bookings(ev)
    return render_template(
            'event_bookings.html',
            event=ev,
            metadata=results['metadata'],
            bookings=results['search_results'],
            )

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
