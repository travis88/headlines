import feedparser
from flask import Flask, render_template, redirect


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

@app.route("/")
@app.route("/<publ>/")
def get_news(publ="yandex"):
    if publ != "favicon.ico":
        feed = feedparser.parse(RSS_FEED[publ])
        return render_template("home.html", articles=feed['entries'])
    return redirect('.get_news', publ)

if __name__ == '__main__':
    app.run(debug=True)
