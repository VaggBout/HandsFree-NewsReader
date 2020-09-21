import re
import heapq
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

from top_articles import BBC_class
from nlp_sum import summary_generator


BBC = BBC_class()
top_article_url = BBC.top_articles_url[1]

title = BBC.get_title(top_article_url)
article = BBC.get_article(top_article_url)
summary = summary_generator(article)
print(summary)