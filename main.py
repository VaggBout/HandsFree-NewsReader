from top_articles import BBC_class
from gtts import gTTS
from io import BytesIO
from pygame import mixer
from multiprocessing import Pool
import time
import os

print('Initialazing Automatic News Anchor...!')
if not os.path.isfile('./greeting_message.mp3'):
    print('First time setup. Please stand by.')
    greetingText = "Hello! I'm your Automatic News Anchor! \
        Your personal hands-free news reader.\
        Today I will summarize and read you the top news from the world!\
        I will now start reading your daily news."
    grettingTTS = gTTS(text=greetingText, lang="en")
    grettingTTS.save('greeting_message.mp3')

mixer.init()
mixer.music.load('./greeting_message.mp3')
mixer.music.play()

BBC = BBC_class()
articles_url = []

i = 0
while i < 3:
    articles_url.append(BBC.top_articles_url[i])
    i += 1

def thread_tts(top_article_url):
    BBC = BBC_class()
    if BBC.get_title(top_article_url) and BBC.get_article(top_article_url):
        # print('Fetching article...')
        title = BBC.get_title(top_article_url)
        title = title+'.'
        article = BBC.get_article(top_article_url)

        # Write article to file for OTS
        f = open("article.txt", "w+")
        f.write(article)
        f.close()
        
        stream = os.popen('ots --ratio 35 article.txt')
        summary = stream.read()
        summary = summary.replace('.', '. ')

        starting_text = "Reading article with title: "
        text = starting_text+title+" "+summary

        fp = BytesIO()
        newsTTS =  gTTS(text=text, lang="en")
        newsTTS.write_to_fp(fp)
        return fp, text

i = 0
with Pool(processes=3) as pool:
    for tts, text in pool.map(thread_tts, articles_url):
        tts.seek(0)
        if mixer.music.get_busy():
            while mixer.music.get_busy():
                time.sleep(1)
                continue
            mixer.music.load(tts)
            mixer.music.play()
            print(text)
        else:
            mixer.music.load(tts)
            mixer.music.play()
            print(text)


while mixer.music.get_busy():
    continue