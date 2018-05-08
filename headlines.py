import feedparser
from flask import Flask


app = Flask(__name__)
RSS_FEED = {
    'yandex': 'https://news.yandex.ru/movies.rss',
    'iol': 'http://rss.iol.io/iol/news',
    'gazeta': 'https://www.gazeta.ru/export/rss/sportnews.xml',
    'cnews': 'http://www.cnews.ru/inc/rss/news_top.xml'
}

@app.route('/')
@app.route('/<publication>')
def get_news(publication='yandex'):
    feed = feedparser.parse(RSS_FEED[publication].encode('utf-8').decode('utf-8'),)
    first_article = feed['entries'][0]
    return """
    <html>
        <head>
            <link id="site-favicon" 
                  href="http://www.allitebooks.com/wp-content/themes/allitebooks/images/favicon.ico" 
                  rel="shortcut icon" type="image/x-icon">
        </head>
        <body>
            <h1> Yandex Movies Headlines</h1>
            <b>{0}</b><br/>
            <i>{1}</i><br/>
            <p>{2}</p><br/>
        </body>
    </html>""".format(first_article.get('title'), 
                      first_article.get('published'),
                      first_article.get('description'))

if __name__ == '__main__':
    app.run(debug=True)
