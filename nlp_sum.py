import re
import heapq
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

def summary_generator(article):

    # Remove quotes from text
    article = re.sub('"', '', article)
    article = re.sub(r'\s+', ' ', article)

    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article)
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    # Tokenize sentences
    sentence_list = nltk.sent_tokenize(article)

    stopwords = nltk.corpus.stopwords.words('english')
    word_frequencies = _word_frequency(formatted_article_text)

    # Weighted frequency
    maximum_frequncy = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    sentence_scores = _score_sentences(sentence_list, word_frequencies)
    threshold = _find_average_score(sentence_scores)
    return _generate_summary(sentence_list, sentence_scores, (threshold))


def _word_frequency(formatted_text):
    stopWords = set(stopwords.words("english"))
    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_text):
        if word not in stopWords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    return word_frequencies

def _score_sentences(sentence_list, word_frequencies):
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    return sentence_scores


def _find_average_score(sentenceValue) -> int:
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    # Average value of a sentence from original text
    average = int(sumValues / len(sentenceValue))

    return average

def _generate_summary(sentences, sentenceValue, threshold):
    # sentence_count = 0
    # summary = ''

    # for sentence in sentences:
    #     if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] > (threshold):
    #         summary += " " + sentence
    #         sentence_count += 1

    summary_sentences = heapq.nlargest(10, sentenceValue, key=sentenceValue.get)
    summary = ' '.join(summary_sentences)
    return summary

# Generate summary
