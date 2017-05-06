import requests
import os
import json

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

## Routes

@app.route('/', methods=['GET'])
def homepage():
    return render_template('homepage.html')

@app.route('/attractions', methods=['GET'])
def attractions():
    results = search_attractions(request.args.get('q'))
    return render_template('attractions.html', attractions=results['_embedded']['attractions'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
