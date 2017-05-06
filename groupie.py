import requests
import os
import json

from urllib.parse import urljoin

from flask import Flask, render_template, redirect, flash, request, abort
from wtforms import TextField, PasswordField, SelectField
from flask_wtf import Form

app = Flask(__name__)
app.secret_key = 'myverylongsecretkey'

BASE_URL = "https://app.ticketmaster.com/"

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY", None)
if not TICKETMASTER_API_KEY:
    print(USAGE)
    exit(1)

## Forms

class AttractionSearch(Form):
    keyword = TextField('Search')

def search_attractions(keyword, locale='en-ie'):
    url = urljoin(BASE_URL, '/discovery/v2/attractions.json')
    resp = requests.get(url, params={
        'apikey': TICKETMASTER_API_KEY,
        'keyword': keyword,
        })

    return resp.json()

## Routes

@app.route('/', methods=['GET', 'POST'])
def homepage():
    form = AttractionSearch()
    if form.validate_on_submit():
        attractions = search_attractions(form.keyword.data)
        return attractions
    return render_template('homepage.html', form=form)

@app.route('/attractions', methods=['POST'])
def attraction_search():
    form = AttractionSearch()
    if form.validate_on_submit():
        results = search_attractions(form.keyword.data)
        return render_template('attractions.html', attractions=results['_embedded']['attractions'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
