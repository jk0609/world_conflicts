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
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
# write method to exclude irrelevant categories, need to filter category names
# more restrictive
#get_articles every 24 hours
#cut down on load times
#fix 404 cases
#README
#Tests


# f = open('gazetteer.txt', 'r')
# allKeywords = f.read().lower().split("\n")
# f.close()

papers = [
    'http://cnn.com',
    'http://www.time.com',
    'http://www.ted.com',
    'http://pandodaily.com',
    'http://www.cnbc.com',
    'http://www.foxnews.com',
    'http://theatlantic.com',
    'http://www.bbc.co.uk',
    'http://www.npr.org',
    'http://www.suntimes.com',
    'http://www.newrepublic.com',
    'http://thecitizen.com',
    'http://thedailyfairfield.com',
    'http://www.news.com.au',
    'http://www.theinsider.com',
    'http://thedailyworld.com',
    'http://nytimes.com',
    'http://yahoo.com',
    'http://www.nbcnews.com',
    'http://thedailypage.com',
    'http://www.pbs.org',
    'http://www.guardiannews.com',
    'http://telegraph.co.uk',
    'http://theatlanticwire.com',
    'http://independent.co.uk',
    'http://thedailyjournal.com',
    'http://thedailynewsegypt.com',
    'http://thedailygrind.com.au',
    'http://tehrantimes.com',
    'http://townhall.com',
    'http://www.reuters.com',
    'http://www.c-span.org',
    'http://washingtontimes.com',
    'http://inquirer.net',
    'http://abcnews.com',
    'http://washingtonexaminer.com',
    'http://hotair.com',
    'http://www.cbc.ca',
    'http://www.slate.com',
    'http://washingtonpost.com',
    'http://www.aljazeera.com',
    'http://thedailyreporter.com',
    'http://www.cbsnews.com',
    'http://www.usnews.com',
    'http://nationalgeographic.com',
    'http://thechronicle.com.au',
    'http://usatoday.com',
    'http://discovermagazine.com',
    'http://foreignpolicy.com',
    'http://www.redstate.com',
    'http://www.bbcamerica.com',
]
article_data = []
build_papers = []

def category_check(article_url):
    output = True
    category_no_words = ['/feed', '/living/','/lifestyle/', 'style', 'video', 'vr', 'entertainment', 'health', 'sport', '/money/','ebook','/travel/','finance','extra','dating','opinion','puzzle','blog','energy','investing','economy','radio','science','education','music','photo','art','business','culture']
    for word in category_no_words:
        if word in article_url:
            output = False
            break
    return output

def includes_keyword(article_keywords):
    counter = 0
    keywords = ['weapons','conflict','rebels','arms','battle','war','rebel','threat','standoff','escalate','trespass']
    for word in keywords:
        if word in article_keywords:
            counter+=1
    if counter>=2:
        return True
    else:
        return False

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

# f = open('categories.txt','r+')
# def get_categories():
#     for paper in papers:
#         current_paper = newspaper.build(paper,fetch_images=False, verbose=True)
#         for url in current_paper.category_urls():
#             f.write(url+'\n')
# get_categories()

def get_papers():
    my_cliff = Cliff('http://localhost',8999)
    found_titles = set()
    # Build each paper in the papers url list using build in multithreading method
    for paper in papers:
        current_paper = newspaper.build(paper,fetch_images=False)
        build_papers.append(current_paper)
    news_pool.set(build_papers,threads_per_source=3)
    news_pool.join()
    #iterate through built papers, parse each article
    for built_paper in build_papers:
        # helper method checking url string
        for article in built_paper.articles:
            # Create new Article object, parse it, add title to found list and check for duplicates before running nlp.
            article.parse()
            if article.title not in found_titles and category_check(article.url)==True:
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
    response = my_cliff.parseText(article.text)
    print(article.url)
    article_data.append(data_dict(response,article.url,article.title,article.summary,'lat','lon','name','country'))


@app.route('/worldconflict/api/v1.0/articles', methods=['GET'])
def get_article_data():
    article_data[:]=[]
    # test()
    get_papers()
    return jsonify({'articles':article_data})

if __name__ == '__main__':
    app.run(debug=True)
