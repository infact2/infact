from bs4 import BeautifulSoup
from openai import OpenAI
from tegtest import *
import json
import requests
import urllib.request

hdr = {'User-Agent': 'Mozilla/5.0'}
omitted_paragraph_keywords = ["all rights reserved", "subscribe", "newsletter", "@", "©", "(c)", "advertis", "cookie", "newsmax", "registered trademark"]

def extractText(url): #takes in link (string) and returns filtered text
    #
    html = urllib.request.urlopen(urllib.request.Request(url, headers=hdr))
    html_parse = BeautifulSoup(html, "html.parser")
    
    text = ""
    for para in html_parse.find_all("p"): 
        para_text = para.get_text()
        para_text_lower = para_text.lower()
        
        # Omit paragraphs with certain keywords
        omit = False
        for word in omitted_paragraph_keywords:
            if word in para_text_lower:
                omit = True
                break
        
        if omit: continue
        text += para_text + "[NEWPARA]"
    
    # Remove excess newlines
    text = text.replace("\n", "").replace("[NEWPARA]", "\n\n")
    #print(text)

    return text

#Retrieves list of articles from tegtest and converts all of it to html
def getText(prompt):
    counter = 1
    paras = ""
    response = getLinks(prompt)
    for article in response['articles']:
              article_url = article["url"]
              text = extractText(article_url)
              paras = paras + "," + " article " + str(counter) + ": " + text
              counter += 1
    #print(paras)
    return paras

#getText(["trump"])
#extractText("https://www.foxnews.com/politics/biden-admin-confirms-terms-maga-trump-kamala-private-bank-transaction-searches#&_intcmp=fnhpbt1,hp1bt")


