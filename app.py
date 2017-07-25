#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify
import newspaper
from newspaper import Config, Article, news_pool
from urllib.request import urlretrieve, urlopen
from urllib.parse import urlparse, urlencode, quote
import json

app = Flask(__name__)

#get_articles every 24 hours
#dont process duplicates(handle with ruby validation?)
#cut down on load times
#fix 404 cases and json error cases


# f = open('gazetteer.txt', 'r')
# allKeywords = f.read().lower().split("\n")
# f.close()

papers = [
    'http://www.huffingtonpost.com',
    'http://cnn.com',
    'http://www.time.com',
    # 'http://www.ted.com',
    # 'http://pandodaily.com',
    # 'http://www.cnbc.com',
    # 'http://www.foxnews.com',
    # 'http://theatlantic.com',
    # 'http://www.bbc.co.uk',
    # 'http://www.npr.org',
    # 'http://www.suntimes.com',
    # 'http://www.newrepublic.com',
    # http://thecitizen.com
    # http://www.morningstar.com
    # http://thedailyfairfield.com
    # http://medicalxpress.com
    # http://www.news.com.au
    # http://www.health.com
    # http://wsj.com
    # http://www.theinsider.com
    # http://cnet.com
    # http://venturebeat.com
    # http://thedailyworld.com
    # http://nytimes.com
    # http://yahoo.com
    # http://www.nbcnews.com
    # http://thedailypage.com
    # http://www.popsci.com
    # http://www.pbs.org
    # http://www.nasa.gov
    # http://www.guardiannews.com
    # http://www.weather.com
    # http://telegraph.co.uk
    # http://theatlanticwire.com
    # http://www.dailyfinance.com
    # http://www.politico.com
    # http://newsroom.fb.com
    # http://independent.co.uk
    # http://thedailyjournal.com
    # http://thedailynewsegypt.com
    # http://thedailygrind.com.au
    # http://tehrantimes.com
    # http://www.today.com
    # http://www.politifact.com
    # http://www.nationalenquirer.com
    # http://egotastic.co
    # http://townhall.com
    # http://www.nypost.com
    # http://www.reuters.com
    # http://www.scientificamerican.com
    # http://www.nydailynews.com
    # http://www.newscientist.com
    # http://bigstory.ap.org
    # http://www.c-span.org
    # http://washingtontimes.com
    # http://thedailyreview.com
    # http://inquirer.net
    # http://abcnews.com
    # http://thedailytimes.com
    # http://washingtonexaminer.com
    # http://hotair.com
    # http://www.cbc.ca
    # http://www.slate.com
    # http://www.forbes.com
    # http://washingtonpost.com
    # http://hbr.org
    # http://www.ft.com
    # http://www.aljazeera.com
    # http://politicker.com
    # http://www.thestreet.com
    # http://www.nj.com
    # http://thedailyreporter.com
    # http://www.economist.com
    # http://phys.org
    # http://www.usmagazine.com
    # http://www.cbsnews.com
    # http://washingtonian.com
    # http://www.sciencedaily.com
    # http://thinkprogress.org
    # http://www.usnews.com=
    # http://nationalgeographic.com
    # http://thechronicle.com.au
    # http://tbnweekly.com
    # http://thedailyfix.com
    # http://www.realclearpolitics.com
    # http://usatoday.com
    # http://discovermagazine.com
    # http://arstechnica.com
    # http://foreignpolicy.com
    # http://www.redstate.com
    # http://www.marketwatch.com
    # http://cbn.com
    # http://www.bbcamerica.com
    # http://washingtonindependent.com
]

build_papers = []

def includes_keyword(article_keywords):
    output = False
    keywords = ['weapons','conflict','rebels','arms','battle','war','rebel','threat','standoff','escalate','trespass']
    for word in keywords:
        if word in article_keywords:
            output = True
            break
    return output

def reporter(article):
    print('test')
    try:
        if article.download() is None:
            return 'no problem'
        else:
            return 'generic'
    except ArticleException():
        return 'false'
    # try:
    #     website_url = "http://foobar.com/article/1234"
    #     site = newspaper.Article(website_url)
    #
    #     page = requests.get(website_url)
    #     page.raise_for_status()
    #
    #     site.download(html=page.content)
    #     site.parse()
    #
    #     # do something with the `site` Article object here...
    #
    # except requests.HTTPError, e:
    #     if e.response.status_code in [404, 410, 400]:
    #         # do something here...
    #         pass

article_data = []


def get_papers():
    # Build each paper in the papers url list using build in multithreading method
    for paper in papers:
        current_paper = newspaper.build(paper,fetch_images=False)
        build_papers.append(current_paper)
    news_pool.set(build_papers,threads_per_source=2)
    news_pool.join()

    #iterate through built papers, parse each article
    for built_paper in build_papers:
        for article in built_paper.articles:
            article.parse()
            article.nlp()

            # If article includes designated keywords, add that data to article_data
            # if includes_keyword(article.keywords):

            # Format text for query string, parse article text with CLIFF
            encodedText = article.text.encode('utf8').decode()
            query = urlencode({ 'q': article.text})
            response = json.loads(urlopen("http://localhost:8999/cliff-2.3.0/parse/text?" + query).read())
            print(article.url, response)
            # append relevant data to json response variable
            article_data.append({
                'latitude': response['results']['places']['focus']['cities'][0]['lat'],
                'longitude': response['results']['places']['focus']['cities'][0]['lon'],
                'city': response['results']['places']['focus']['cities'][0]['name'],
                'country': response['results']['places']['focus']['countries'][0]['name'],
                'url': article.url,
                'title': article.title,
                'summary': article.summary
            })

def test():
    article = Article('http://www.cnn.com/2017/07/25/politics/senate-health-care-vote/index.html')
    article.download()
    article.parse()
    article.nlp()

    # Format text for query string, parse article text with CLIFF
    encodedText = article.text.encode('utf8').decode()
    query = urlencode({ 'q': article.text})
    response = json.loads(urlopen("http://localhost:8999/cliff-2.3.0/parse/text?" + query).read())
    print(response)
    # append relevant data to json response variable
    article_data.append({
        'latitude': response.get(['results']['places']['focus']['cities'][0]['lat'],'None'),
        'longitude': response['results']['places']['focus']['cities'][0]['lon'],
        'city': response['results']['places']['focus']['cities'][0]['name'],
        'country': response['results']['places']['focus']['countries'][0]['name'],
        'url': article.url,
        'title': article.title,
        'summary': article.summary
    })


@app.route('/')
def index():
    return "Hello, World!"

# define route, run function defined above and return as json. Get requests only

@app.route('/todo/api/v1.0/cnn', methods=['GET'])
def get_article_data():
    # test()
    get_papers()
    return jsonify({'articles':article_data})

if __name__ == '__main__':
    app.run(debug=True)
