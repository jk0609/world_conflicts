#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify
import newspaper
from newspaper import Config, Article, news_pool
from urllib.request import urlretrieve, urlopen
from urllib.parse import urlparse, urlencode, quote
import json
from mediameter.cliff import Cliff

app = Flask(__name__)
#get_articles every 24 hours
#cut down on load times
#fix 404 cases


# f = open('gazetteer.txt', 'r')
# allKeywords = f.read().lower().split("\n")
# f.close()

papers = [
    'http://cnn.com',
    'http://www.time.com',
    # 'http://www.ted.com',
    # 'http://pandodaily.com',
    'http://www.cnbc.com',
    # 'http://www.foxnews.com',
    # 'http://theatlantic.com',
    'http://www.bbc.co.uk',
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
    'http://www.politifact.com',
    # http://www.nationalenquirer.com
    # http://egotastic.co
    # http://townhall.com
    # http://www.nypost.com
    'http://www.reuters.com',
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
    'http://www.aljazeera.com',
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

def data_dict(response,url,title,summary,*keys):
    print(url,title,summary)
    new_dict = {}
    for key in keys:
        try:
            if key=='country':
                new_dict[key] = response['results']['places']['focus']['countries'][0]['name']
            else:
                new_dict[key] = response['results']['places']['focus']['cities'][0][key]
        except (KeyError,IndexError):
            new_dict[key] = 'None'
    new_dict['url'] = url
    new_dict['title'] = title
    new_dict['summary'] = summary
    return new_dict

def get_papers():
    my_cliff = Cliff('http://localhost',8999)
    found_titles = set()
    # Build each paper in the papers url list using build in multithreading method
    for paper in papers:
        current_paper = newspaper.build(paper,fetch_images=False, verbose=True)
        build_papers.append(current_paper)
    news_pool.set(build_papers,threads_per_source=2)
    news_pool.join()
    #iterate through built papers, parse each article
    for built_paper in build_papers:
        for article in built_paper.articles:
            # Create new Article object, download/parse it, add title to found list and check for duplicates before running nlp.
            article.download()
            article.parse()
            if article.title not in found_titles:
                article.nlp()
                # If article includes designated keywords, add that data to article_data
                if includes_keyword(article.keywords):
                    found_titles.add(article.title)
                    response = my_cliff.parseText(article.text)
                    print(article.url)
                    # append relevant data to json response variable
                    article_data.append(data_dict(response,article.url,article.title,article.summary,'lat','lon','name','country'))

def test():
    my_cliff = Cliff('http://localhost',8999)
    article = Article('http://www.cnn.com/2017/07/25/politics/senate-health-care-vote/index.html')
    article.download()
    article.parse()
    article.nlp()

    # Format text for query string, parse article text with CLIFF
    # encodedText = article.text.encode('utf8').decode()
    # query = urlencode({ 'q': article.text})
    response = my_cliff.parseText(article.text)
    print(article.url)
    # append relevant data to json response variable
    article_data.append(data_dict(response,article.url,article.title,article.summary,'lat','lon','name','country'))

# my_cliff = Cliff('http://localhost',8999)
# response = my_cliff.parseText("This is about Einstien at the IIT in New Delhi.")
# print(response.get('results').get('places').get('focus'))



@app.route('/')
def index():
    return "Hello, World!"

# define route, run function defined above and return as json. Get requests only

@app.route('/worldconflict/api/v1.0/article', methods=['GET'])
def get_article_data():
    # test()
    get_papers()
    return jsonify({'articles':article_data})

if __name__ == '__main__':
    app.run(debug=True)
