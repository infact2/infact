import urllib.request
import re
import random
import spacy
from bs4 import BeautifulSoup 

# url = "https://www.foxnews.com/world/hamas-releases-more-israeli-hostages-6th-day-cease-fire"
# url = "https://www.newsmax.com/us/joe-biden-impeachment-house/2023/11/29/id/1144091/"
# url = "https://www.cnn.com/2023/11/29/politics/vivek-ramaswamy-aide-trump-campaign/index.html"

nlp = spacy.load("en_core_web_sm")

omitted_paragraph_keywords = ["all rights reserved", "subscribe", "newsletter", "@", "©", "(c)"]

margin = 2

def extractText(url):
    html = urllib.request.urlopen(url) 
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
    text = text.replace("\n", "")

    return text

# ==========================================================================

def processData(text):
    paragraphs = text.split("[NEWPARA]")
    paragraph_data = []


    paragraph_index = 0
    for paragraph in paragraphs:
        document = nlp(paragraph)
        paragraph_data.append({
            "subjects": [],
            "subject_vectors": spacy.vectors.Vectors(shape=(10000, 300))
        })

        for token in document:
            if token.is_space: continue
            if token.dep_ == "nsubj": # if subject
                paragraph_data[paragraph_index]["subjects"].append(token)
                paragraph_data[paragraph_index]["subject_vectors"].add(token.text)
        paragraph_index += 1

    # document = nlp(text)
    # vectors = spacy.vectors.Vectors(shape=(10000, 300))

    # for token in document:
    #     vectors.add(token.text)
        # print(token.text)
    # for token in document:
    #     if token.is_space: continue
    #     print(f"{token}: {token.dep_}", end="")
    #     if token.is_sent_end:
    #         print(" [yes end sentence wopooo]")
    #     else:
    #         print("")

    return data

# ==========================================================================



def identifyPhrases(text):
    phrases = []

def plugAndPlay(text):
    pass

def corroborate(text1, text2):
    return generateSequence("the", 10, text1 + text2, "balls")
    # impleeemtnt laterrrrrr

# print(corroborate(
#     extractText("https://www.cnn.com/2023/11/29/politics/vivek-ramaswamy-aide-trump-campaign/index.html"),
#     extractText("https://www.newsmax.com/us/joe-biden-impeachment-house/2023/11/29/id/1144091/")
# ))

processData("I love oily black men. I like hurling bricks at children, which is an illegal crime. Please kill yourself now. Etc. is shorthand for etcetera!")