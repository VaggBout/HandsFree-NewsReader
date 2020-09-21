import requests
from bs4 import BeautifulSoup as bs

class BBC_class:

    bbc_base_url = "https://www.bbc.com"

    def __init__(self):
        news_feed = requests.get(self.bbc_base_url + '/news')
        self.soup = bs(news_feed.content, "html.parser")
        self.top_articles_url = self.get_top_articles_url()


    def get_top_articles_url(self) -> list:
        top_articles_url = []
        for link in self.soup.findAll("a", {'class' : "gs-c-promo-heading nw-o-link gs-o-bullet__text gs-o-faux-block-link__overlay-link gel-pica-bold gs-u-pl-@xs"}):
            top_articles_url.append(link.get('href'))
        return top_articles_url

    def get_article(self, endpoint):
        get_article = requests.get(self.bbc_base_url + endpoint)
        if get_article.status_code != 200:
            return None
        else:
            article = bs(get_article.content, 'html.parser')
            body = article.find(property="articleBody")
            article_text = ""

            for p in body.find_all("p"):
                article_text += p.text
        
        return article_text


    def get_title(self, endpoint):
        get_article = requests.get(self.bbc_base_url + endpoint)
        if get_article.status_code != 200:
            return None
        else:
            article = bs(get_article.content, 'html.parser')
            return article.find(class_="story-body__h1").text