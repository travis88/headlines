import feedparser
import json
import os
import urllib
from urllib.request import urlopen
from flask import Flask, render_template, request


app = Flask(__name__)
RSS_FEED = {
    "fox": "http://feeds.foxnews.com/foxnews/latest",
    "habr": "https://habr.com/rss/hubs/all/",
    "yandex": "https://news.yandex.ru/movies.rss",
    "iol": "http://rss.iol.io/iol/news",
    "gazeta": "https://www.gazeta.ru/export/rss/sportnews.xml",
    "cnews": "http://www.cnews.ru/inc/rss/news_top.xml",
    "nasa": "https://www.nasa.gov/rss/dyn/earth.rss"
}
OPEN_WEATHER_MAP_KEY = os.environ.get('OPEN_WEATHER_MAP_KEY')
OPEN_EXCHANGE_RATES = os.environ.get('OPEN_EXCHANGE_RATES')
DEFAULTS = {
    'publ': 'yandex',
    'city': 'Moscow',
    'currency_from': 'GBP',
    'currency_to': 'USD'
}


def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    query = urllib.parse.quote(query)
    url = api_url.format(query, OPEN_WEATHER_MAP_KEY)
    r = urlopen(url)
    data = r.read().decode(r.info().get_param('charset') or 'utf-8')
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {
            'description': parsed['weather'][0]['description'],
            'temperature': parsed['main']['temp'],
            'city': parsed['name'],
            'country': parsed['sys']['country']
        }
    return weather


def get_rate(frm, to):
    app_url = "http://data.fixer.io/api/latest?access_key={}"
    url = app_url.format(OPEN_EXCHANGE_RATES)
    r = urlopen(url)
    all_currency = r.read().decode(r.info().get_param('charset') or 'utf-8')
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return to_rate/frm_rate

def get_news(query):
    if not query or query.lower() not in RSS_FEED:
        publ = DEFAULTS['publ']
    else:
        publ = query.lower()
    feed = feedparser.parse(RSS_FEED[publ])
    return feed['entries']


@app.route("/", methods=['GET', 'POST'])
def home():
    publ = request.form.get('publ')
    articles = get_news(publ)
    
    city = request.form.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather('{},RU'.format(city))

    currency_from = request.form.get('currency_from')
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.form.get('currency_to')
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate = get_rate(currency_from, currency_to)

    return render_template("home.html", 
                           articles=articles, 
                           weather=weather,
                           currency_from=currency_from,
                           currency_to=currency_to,
                           rate=rate)

if __name__ == '__main__':
    app.run(debug=True)
