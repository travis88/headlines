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
            'city': parsed['name']
        }
    return weather


@app.route("/", methods=['GET', 'POST'])
def get_news():
    query = request.form.get('publ')
    if not query or query not in RSS_FEED:
        publ = 'yandex'
    else:
        publ = query.lower()
    feed = feedparser.parse(RSS_FEED[publ])
    weather = get_weather('Moscow,RU')
    return render_template("home.html", 
                           articles=feed['entries'], 
                           weather=weather)

if __name__ == '__main__':
    app.run(debug=True)
