from bs4 import BeautifulSoup
from openai import OpenAI
from newsapi import *
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

def getTextCse(prompt): #WIP
    counter = 1
    paras = ""
    response = getDaLinks(prompt)
    for article_url in response:
              text = extractText(article_url)
              paras = paras + "," + " article " + str(counter) + ": " + text
              counter += 1
    #print(paras)
    return paras

def getFullHTML(url):
    html = urllib.request.urlopen(urllib.request.Request(url, headers=hdr))
    html_parse = BeautifulSoup(html, "html.parser")
    return html_parse

#getText(["trump"])
extractText("https://news.google.com/__i/rss/rd/articles/CBMiZ2h0dHBzOi8vd3d3LmRlZmVuc2UuZ292L05ld3MvTmV3cy1TdG9yaWVzL0FydGljbGUvQXJ0aWNsZS8zMjc2NDc3L3VzLWlzcmFlbC1iZWdpbi1qdW5pcGVyLW9hay1leGVyY2lzZS_SAQA?oc=5")


