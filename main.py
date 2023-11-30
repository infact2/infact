import urllib.request
import re
from bs4 import BeautifulSoup 

# url = "https://www.foxnews.com/world/hamas-releases-more-israeli-hostages-6th-day-cease-fire"
# url = "https://www.newsmax.com/us/joe-biden-impeachment-house/2023/11/29/id/1144091/"
# url = "https://www.cnn.com/2023/11/29/politics/vivek-ramaswamy-aide-trump-campaign/index.html"
omitted_paragraph_keywords = ["all rights reserved", "subscribe", "newsletter", "@", "©", "(c)"]
seperating_punctuation = ".?<>()[];:\"!"

def extractText(url, keep_newlines = true):
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
        text += para_text + "[NEWLINEHEREEEEE]"
    
    if keep_newlines:
        # Remove excess newlines
        text = text.replace("\n", "").replace("[NEWLINEHEREEEEE]", "\n")
    else:
        text = text.replace("\n", "").replace("[NEWLINEHEREEEEE]", "")

    return text

def corroborate(url1, url2):
    article1 = extractText(url1)
    article2 = extractText(url2)

    # impleeemtnt laterrrrrr

print(extractText("https://www.cnn.com/2023/11/29/politics/vivek-ramaswamy-aide-trump-campaign/index.html"))